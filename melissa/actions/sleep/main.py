import random

# Melissa
from melissa.profile import data

WORDS = {'go_to_sleep': {'groups': ['sleep', 'bye', 'deactivate', 'stop',
         'suspend', 'quit', ['power', 'off'], ['stand', 'down'],
         ['good', 'bye']]}}


class Sleep():

    def go_to_sleep(self, text):
        replies = ['See you later!', 'Just call my name and I\'ll be there!']
        if data['hotword_detection'] == 'on':
            print('\nListening for Keyword...')
            print('Press Ctrl+C to exit')

        quit()
        return random.choice(replies)
