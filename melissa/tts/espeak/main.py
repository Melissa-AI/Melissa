import subprocess

import pyvona

# Melissa
from melissa import profile
from melissa.tts_facade import TTS


class EspeakTTS(TTS):

    def speak(self, message):
        """
        This function takes a message as an argument and converts it to
        speech depending on the OS and engine.
        """
        if profile.data['tts'] == 'ivona':
            access_key = profile.data['ivona']['access_key']
            secret_key = profile.data['ivona']['secret_key']
            tts_engine = pyvona.create_voice(access_key, secret_key)
            if profile.data['va_gender'] == 'female':
                tts_engine.voice_name = 'Salli'
            else:
                tts_engine.voice_name = 'Joey'
            tts_engine.speak(message)

        else:
            engine = 'espeak'
            if profile.data['va_gender'] == 'female':
                language = '-ven+f3'
                speed = '-s170'
                return subprocess.call([engine, language, speed, message])
            else:
                speed = '-s170'
                return subprocess.call([engine, speed, message])
