import subprocess
import pyvona
# Melissa
from melissa.profile import data
from melissa.tts import TTS


class IvonaTTS(TTS):

    name = 'ivona'    

    def speak(self, message):
        """
        This function takes a message as an argument and converts it to
        speech.
        """
        access_key = data['ivona']['access_key']
        secret_key = data['ivona']['secret_key']
        engine = pyvona.create_voice(access_key, secret_key)
        if profile.data['va_gender'] == 'female':
            engine.voice_name = 'Salli'
        else:
            engine.voice_name = 'Joey'
        engine.speak(message)
