import subprocess
# Melissa
from melissa.profile import data
from melissa.tts import TTS


class SayTTS(TTS):
    
    name = 'say'

    def speak(self, message):
        """
        This function takes a message as an argument and converts it to
        speech.
        """
        engine = 'say'
        if data['va_gender'] == 'male':
            language = '-valex'
            return subprocess.call([engine, language, message])
        else:
            return subprocess.call([engine, message])
