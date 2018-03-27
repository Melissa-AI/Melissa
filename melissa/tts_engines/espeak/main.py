import subprocess
# Melissa
from melissa import profile
from melissa.tts_facade import TTS


class EspeakTTS(TTS):

    def __init__(self):
        self.name = 'espeak'

    def speak(self, message):
        """
        This function takes a message as an argument and converts it to
        speech depending on the OS and engine.
        """
        engine = 'espeak'
        if profile.data['va_gender'] == 'female':
            language = '-ven+f3'
            speed = '-s170'
            return subprocess.call([engine, language, speed, message])
        else:
            speed = '-s170'
            return subprocess.call([engine, speed, message])
