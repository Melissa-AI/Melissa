# Melissa
from profile import data
from tts_engines.espeak.main import EspeakTTS
from tts_engines.say.main import SayTTS
from tts_engines.ivona.main import IvonaTTS

tts_module = __import__('melissa.tts_engines')

EspeakTTS = getattr(tts_module, EspeakTTS)
SayTTS = getattr(tts_module, SayTTS)
IvonaTTS = getattr(tts_module, IvonaTTS)

if data['tts'] == 'ivona':
    tts_engine = IvonaTTS()
elif data['tts'] == 'espeak':
    tts_engine = EspeakTTS()
elif data['tts'] == 'say':
    tts_engine = SayTTS()
else:
    pass

while True:
    text = ''  # Text returned by STT Engine

    tts_engine.speak(text)  # User's query

    response = ''  # Response given by actions corresponding to text

    tts_engine.speak(response)  # TTS Engine gives the response
    print(response)
