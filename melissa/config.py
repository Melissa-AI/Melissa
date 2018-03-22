import sys

# Melissa
from profile import data
from tts.espeak.main import EspeakTTS
from tts.say.main import SayTTS
from tts.ivona.main import IvonaTTS

if data['tts'] == 'ivona':
    tts_engine = IvonaTTS()
else:
    if sys.platform == 'darwin':
        tts_engine = SayTTS()
    elif sys.platform.startswith('linux') or sys.platform == 'win32':
        tts_engine = EspeakTTS()
