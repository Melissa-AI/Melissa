from multiprocessing import Process, Lock, Pipe, Value, active_children
import sqlite3
from time import sleep

# Melissa
import melissa.profile as profile
import melissa.stt as stt
from melissa.tts import tts
import melissa.actions_db as actions_db
from melissa.response_deque import RD
import melissa.brain as brain

# running is changed to 0 (False) when the user requests Melissa to quit.
# A 'Value' format variable provides access for all threads.
running = Value('i', 1)

# interjection is used to provide a speaking (tts) delay between
# immediate and queued responses.
interjection = Value('i', 0)

# The number of delay seconds between speaking responses.
response_delay_secs = 4

# lock is used to avoid a collision between immediate and queued
# speaking responses. Since speaking is inherently single threaded,
# this locking does not cause an efficiency issue.
lock = Lock()

# A pipe is required to connect keyboard prompts and replies from the
# main thread, where keyboard entry must be accepted, to the request
# thread.
(pipe_end1, pipe_end2) = Pipe()

rd = RD() # A multiprocessing capable response deque

def melissa_sleep(secs):
    '''
    Check if a Melissa shutdown has been set each second for a sleep
    duration and if so return. This avoids a longer shutdown wait.
    '''

    for i in range(0,secs):
        if running.value:
            sleep(1)
        else:
            return


def request():
    '''
    This thread performs the audio request and response loop.

    stt_engine.transcribe() waits until the user speaks,
        processes the speech through a recognizer,
        returns the recognized text.

    brain.query takes the speech text,
        matches it against the available actions,
        returns the most likely intended action.

    If the return from brain.query indicates that a thread should be used
        a thread is created for the returned function.
    Otherwise the function is executed and its text response given to tts.

    The locking for giving the response text to tts is avoid a conflict
        at tts if the response loop obtains a text from the response
        deque at the same time.
    '''

    tts('Hello' + profile.data['name'] + ', systems are now ready to run. How can I help you?')

    stt_engine = False
    if profile.data['stt'] == 'keyboard':
        pipe_end2.send('Enter your query')
    else:
        stt_engine = stt.get_engine_by_name(profile.data['stt']).get_instance()

    while(running.value):
        speech_text = ''
        if profile.data['stt'] == 'keyboard':
            speech_text = pipe_end2.recv()
        else:
            # stt waits for the user to provide input
            speech_text = stt_engine.transcribe()

        (module_name, function, properties) = brain.query(speech_text)

        # A brain selected function can be threaded here for which any
        # speech responses will need to be placed in the response deque.
        if properties['threaded']:
            p = Process(target=getattr(actions_db.modules[module_name], function), args=(speech_text)) # Use dynamic module call.
            p.start()
            # function return goes to deque

        # A 'returns' function returns speech text to be given to tts.
        elif properties['returns']:
            response_text = getattr(actions_db.modules[module_name], function)(speech_text)
            if len(response_text):
                lock.acquire()
                interjection.value = 1
                tts(response_text)
                lock.release()

        # A function may do its own speaking (not silent).
        elif not properties['silent']:
            lock.acquire()
            interjection.value = 1
            getattr(actions_db.modules[module_name], function)(speech_text)
            lock.release()

        # Otherwise the function does not speak and performs a
        # quick task.
        else:
            getattr(actions_db.modules[module_name], function)(speech_text)

        active_children() # Join all finished processes.

        if module_name == 'sleep':
            running.value = 0
            if profile.data['stt'] == 'keyboard':
                pipe_end2.send('') # Clear waiting pipe to allow quit.
            return

        if profile.data['stt'] == 'keyboard':
            pipe_end2.send('Enter your query')


def notification_polling(function, poll_period):
    '''
    This function is contained in a thread for each notification. This
    allows a different polling period for each notification.

    The notification return is placed on the response deque,
    '''

    module_name, function = function.split()

    # The priming-read pattern removes an ending sleep on Melissa quit.
    getattr(actions_db.modules[module_name], function)()
    while(running.value):
        melissa_sleep(poll_period)
        getattr(actions_db.modules[module_name], function)()


def notifications():
    '''
    A thread for each notification is created here.

    All the notifications in the actions_db are selected and a thread is
    created for each notification.
    '''

    # Get notifications.
    sql = "SELECT function, poll_period "\
         +"FROM notifications"

    actions_db.cur.execute(sql)
    rows = actions_db.cur.fetchall()

    for row in rows:
        # Debug line left for when notifications is actually used.
        print 'launched notification ' + row[0]
        p = Process(target=notification_polling, args=(row[0],row[1]))
        p.start()

    active_children() # Join all finished processes.


def response_detail():
    '''
    The response detail will likely gain more code for a variety of
    items. Separating that here streamlines the code.

    A short delay is provided between each audio response so that the
    user recognizes they are different and can absorb each response
    before hearing the next one.
    '''

    item = rd.popleft()
    # Debug lines left for when response_detail is actually used.
    print 'response item'
    print type(item)
    print item
    if type(item) == type({}):
        if 'speech_text' in item:
            if len(item['speech_text']):
                if interjection.value:
                    interjection.value = 0
                    melissa_sleep(response_delay_secs)

                lock.acquire()
                tts(item['speech_text'])
                lock.release()


def response():
    '''
    The response thread checks if there are any entries in the response
    deque and if there are any, pops the first entry on the left and
    sends the response text to be processed by response_detail().
    '''

    while(running.value):
        if rd.getvalue():
            response_detail()
            melissa_sleep(response_delay_secs)


def main():
    '''
    Three threads are created here, one for each of
        audio/keyboard requests,
        notifications,
        and qeued (deque) responses.
    '''

    request_thread = Process(target=request, args=())
    request_thread.start()

    notifications_thread = Process(target=notifications, args=())
    notifications_thread.start()

    response_thread = Process(target=response, args=())
    response_thread.start()

    # For keyboard entry, a pipe is required between this top thread
    # and the request thread.
    if profile.data['stt'] == 'keyboard':
        prompt = pipe_end1.recv()
        while(running.value):
            keyboard_text = raw_input(prompt+': ')
            pipe_end1.send(keyboard_text)
            prompt = pipe_end1.recv()

    request_thread.join()
    notifications_thread.join()
    response_thread.join()


main()

