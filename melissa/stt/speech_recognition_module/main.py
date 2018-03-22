'''
This module contains implementation of Speech Recognition using
SpeechRecognition package
'''
import speech_recognition as sr
from melissa.stt_facade import STT


class SpeechRecognitionSST(STT):

    def write(self):
        """
        This function converts some speech to text depending on the OS.
        returns text: string
        """
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)

        # Speech recognition using Google Speech Recognition
        try:
            text = r.recognize_google(audio)
            print('You said: ' + text)
            return text
        except Exception as e:
            print('Google Speech Recognition could not understand' +
                  'audio due to {0}'.format(e))
            text = "Google Speech Recognition could not understand"
            return text
