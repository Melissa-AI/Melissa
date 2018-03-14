import sys

# Melissa
from tts.espeak.main import EspeakTTS
from tts.say.main import SayTTS

if sys.platform == 'darwin':
    tts_engine = SayTTS()
elif sys.platform.startswith('linux') or sys.platform == 'win32':
    tts_engine = EspeakTTS()
