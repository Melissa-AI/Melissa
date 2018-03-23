import os
from os.path import basename
import sys
import random

# Melissa
from melissa.profile import data

WORDS = {
    'play_shuffle': {
        'groups': [
            ['party', 'time'],
            ['party', 'mix']
        ]
    },
    'play_random': {
        'groups': [
            ['play', 'music'],
            'music']
    },
    'play_specific_music': {
        'groups': ['play']
    }
}

sox_file_types = ['.wav', '.flac', 'ogg']
music_listing = None


class PlayMusic():

    def mp3gen(self):
        """
        This function finds all the mp3 files in a folder
        and it's subfolders and returns a list.
        """
        global music_listing

        if music_listing is not None:
            return

        if sys.platform != 'darwin' \
                and sys.platform != 'win32' \
                and not sys.platform.startswith('linux'):
            print "Music only enabled on darwin, win32, and linux."
            return

        music_listing = []
        for root, dirs, files in os.walk(data['music_path']):
            for filename in files:
                if os.path.splitext(filename)[1] == ".mp3":
                    if sys.platform == 'darwin':
                        music_listing.append([
                            'afplay',
                            os.path.join(root, filename.lower())])
                    else:
                        music_listing.append([
                            'mpg123',
                            os.path.join(root, filename.lower())])
                elif os.path.splitext(filename)[1] in sox_file_types:
                    if sys.platform != 'darwin':
                        music_listing.append([
                            'play',
                            os.path.join(root, filename.lower())]
                        )

    def music_player(music_selection):
        """
        This function takes the name of a music file as an argument
        and plays it depending on the OS.
        """
        player = music_selection[0] + " '" + music_selection[1] + "'"
        return os.system(player)

    def play_random(self, text):
        try:
            self.mp3gen()
            music_playing = random.choice(music_listing)
            song_name = os.path.splitext(basename(music_playing[1]))[0]
            return "Now playing: " + song_name
            self.music_player(music_playing)

        except IndexError as e:
            print("No music files found: {0}".format(e))
            return 'No music files found.'

    def play_specific_music(self, speech_text):
        words_of_message = speech_text.split()
        words_of_message.remove('play')
        cleaned_message = ' '.join(words_of_message)
        self.mp3gen()

        for i in range(0, len(music_listing)):
            if cleaned_message in music_listing[i][1]:
                self.music_player(music_listing[i])

    def play_shuffle(self, text):
        try:
            self.mp3gen()
            random.shuffle(music_listing)
            for i in range(0, len(music_listing)):
                self.music_player(music_listing[i])

        except IndexError as e:
            print("No music files found: {0}".format(e))
            return 'No music files found.'
