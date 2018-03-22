import subprocess
# Melissa
from melissa import profile
from melissa.tts_facade import TTS


class SayTTS(TTS):

    def speak(self, message):
        """
        This function takes a message as an argument and converts it to
        speech.
        """
        engine = 'say'
        if profile.data['va_gender'] == 'male':
            language = '-valex'
            return subprocess.call([engine, language, message])
        else:
            return subprocess.call([engine, message])
