import random
import requests
import json

# Melissa
from melissa import profile
from melissa.tts import tts

WORDS = {'who_are_you': {'groups': [['who', 'are', 'you']]},
         'toss_coin': {'groups': [['heads', 'tails'],
                                  ['toss', 'coin'], ['flip', 'coin']]},
         'how_am_i': {'groups': [['how', 'i', 'look'], ['how', 'am', 'i']]},
         'tell_joke': {'groups': [['tell', 'joke']]},
         'who_am_i': {'groups': [['who', 'am', 'i']]},
         'where_born': {'groups': [['where', 'born']]},
         'how_are_you': {'groups': [['how', 'are', 'you']]},
         'are_you_up': {'groups': [['you', 'up']]},
         'love_you': {'groups': [['love', 'you']]},
         'marry_me': {'groups': [['marry', 'me']]},
         'undefined': {'groups': []}}


def who_are_you(text):
    va_name = profile.data['va_name']
    messages = ['I am ' + va_name + ', your lovely personal assistant.',
                va_name + ', didnt I tell you before?',
                'You ask that so many times! I am ' + va_name]
    tts(random.choice(messages))


def toss_coin(text):
    outcomes = ['heads', 'tails']
    tts('I just flipped a coin. It shows ' + random.choice(outcomes))


def how_am_i(text):
    replies = [
        'You are goddamn handsome!',
        'My knees go weak when I see you.',
        'You are sexy!',
        'You look like the kindest person that I have met.'
    ]
    tts(random.choice(replies))


def tell_joke(text):
    first_time = True
    seen_chuck_norris_joke = False
    while(True):
        if first_time and not seen_chuck_norris_joke:
            print 'Perhaps a Chuck Norris one? \nAnswer with a yes or a no?'
        elif not first_time and not seen_chuck_norris_joke:
            print 'Atleast now a Chuck Norris one?'
        elif not first_time and seen_chuck_norris_joke:
            print 'Another Chuck Norris joke?'
        chuck_norris_flag = raw_input()
        if chuck_norris_flag == '' or chuck_norris_flag == 'no':
            print 'Alright, your choice. But, if you ask me, you are',
            if not first_time:
                print 'really',
            else:
                print 'really, really',
            print 'missing something!"'
            jokes = [
                'What happens to a frogs car when it breaks down?'
                ' It gets toad away.',
                'Why was six scared of seven? Because seven ate nine.',
                'Why are mountains so funny?'
                ' Because they are hill areas.',
                'Have you ever tried to eat a clock? '
                'I hear it is very time consuming.',
                'What happened when the wheel was invented?'
                ' A revolution.',
                'What do you call a fake noodle? An impasta!',
                'Did you hear about that new broom?'
                ' It is sweeping the nation!',
                'What is heavy forward but not backward? Ton.',
                'No, I always forget the punch line.'
            ]
            print random.choice(jokes)
            tts(random.choice(jokes))
            first_time = False
            seen_chuck_norris_joke = False
        else:
            if not first_time:
                print 'Good.'
            req = requests.get('http://api.icndb.com/jokes/random')
            json_joke = json.loads(req.text)['value']
            print 'Here is a',
            if json_joke['categories']:
                print json_joke['categories'][0],
            print 'Chuck Norris joke for you: '
            print json_joke['joke']
            tts(json_joke['joke'])
            seen_chuck_norris_joke = True
            first_time = False

        go_again = raw_input('Haha, do you want another one?: ')
        if go_again == 'yes':
            continue
        else:
            print 'That was good, no? Haha, again!'
            break


def who_am_i(text):
    name = profile.data['name']
    tts('You are ' + name + ', a brilliant person. I love you!')


def where_born(text):
    tts('I was created by a magician named Tanay, in India, '
        'the magical land of himalayas.')


def how_are_you(text):
    tts('I am fine, thank you.')


def are_you_up(text):
    tts('For you sir, always.')


def love_you(text):
    replies = [
               'I love you too.',
               'You are looking for love in the wrong place.'
              ]
    tts(random.choice(replies))


def marry_me(text):
    tts('I have been receiving a lot of marriage proposals recently.')


def undefined(text):
    tts('I dont know what that means!')
