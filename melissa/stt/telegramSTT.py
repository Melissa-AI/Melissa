import os
from melissa.profile import data
import speech_recognition as sr
from melissa import brain

class TelegramMessenger():

    def handle(self, msg):
        username = msg['chat']['username']
        command = msg['text'].lower().replace("'", "")
        if username == data['telegram_username']:
            print(data['va_name'] + " thinks you said '"
                + command + "'")
        brain.query(command)

    def send(self, msg):
        while True:
            if data['telegram_token'] == '':
                quit()
            else:
                bot = telepot.Bot(data['telegram_token'])
                bot.notifyOnMessage(handle)
                while 1:
                 time.sleep(10)
