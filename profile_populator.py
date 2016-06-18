import os
import json
from getpass import getpass

# Melissa
from tts import tts

def profile_populator():
    def empty(variable):
        if variable:
            return False
        else:
            return True

    tts('Welcome to Melissa. Let us generate your profile!')
    print('Welcome to Melissa. Let us generate your profile!')
    print('Press Enter for using default values.')

    name = raw_input('Your name: ')
    if empty(name):
        name = 'Tanay'

    while(True):
        stt = raw_input('STT Engine ((g)oogle/(s)phinx/(k)eyboard): ').lower()
        if stt in ('g','google', 's','sphinx', 'k','keyboard', ''):
            if empty(stt) or stt == 'g':
                stt = 'google'
            elif stt == 's':
                stt = 'sphinx'
            elif stt == 'k':
                stt = 'keyboard'
            break
        print('Invalid input, please enter (g)oogle, (s)phinx, (k)eyboard or <ENTER>.')

    while(True):
        music_path = raw_input('Path to your music directory: ')
        if empty(music_path):
            music_path = '.'
            break
        if os.path.isdir(music_path):
            break
        print('Invalid input, please enter a valid directory path or <ENTER>.')

    while(True):
        images_path = raw_input('Path to your images directory: ')
        if empty(images_path):
            images_path = '.'
            break
        if os.path.isdir(images_path):
            break
        print('Invalid input, please enter a valid directory path or <ENTER>.')

    city_name = raw_input('Name of city where you live: ')
    if empty(city_name):
        city_name = 'New Delhi'

    city_code = raw_input('Code of city from weather.com: ')
    if empty(city_code):
        city_code = 'INXX0096'

    while(True):
        degrees = raw_input('(c)elsius/(f)ahrenheit): ').lower()
        if degrees in ('c','celsius', 'f','fahrenheit', ''):
            if empty(degrees) or degrees == 'c':
                degrees = 'celsius'
            elif degrees == 'f':
                degrees = 'fahrenheit'
            break
        print('Invalid input, please enter (c)elsius, (f)ahrenheit) or <ENTER>.')

    gmail_address = raw_input('Enter your gmail address (???@gmail.com): ')
    gmail_password = getpass()

    access_token = 'xxxx'
    access_token_secret = 'xxxx'
    consumer_key = 'xxxx'
    consumer_secret = 'xxxx'

    client_id = 'xxxx'
    client_secret = 'xxxx'

    modeldir = '/usr/local/share/pocketsphinx/model/'
    hmm = 'en-us/en-us'
    lm = 'lm/2854.lm'
    dic = 'lm/2854.dic'

    modules = 'modules'
    words_db_file = ':memory:'
    memory_db = './memory.db'

    profile_data = {
        'name': name,
        'stt': stt,
        'music_path': music_path,
        'images_path': images_path,
        'city_name': city_name,
        'city_code': city_code,
        'degrees': degrees,
        'pocketsphinx': {
            'modeldir': modeldir,
            'hmm': hmm,
            'lm': lm,
            'dic': dic
        },
        'twitter': {
            'access_token': access_token,
            'access_token_secret': access_token_secret,
            'consumer_key': consumer_key,
            'consumer_secret': consumer_secret
        },
        'imgur': {
            'client_id': client_id,
            'client_secret': client_secret
        },
        'gmail': {
            'address': gmail_address,
            'password': gmail_password
        },
        'modules': modules,
        'words_db_file': words_db_file,
        'memory_db': memory_db
    }

    with open('profile.json', 'w') as outfile:
        json.dump(profile_data, outfile, indent=4)
