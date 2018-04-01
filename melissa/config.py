# Melissa
from profile import data
from stt.speech_recognition_module.googleSTT import GoogleSTT
from stt.speech_recognition_module.sphinxSTT import SphinxSTT
from stt.watson.main import WatsonSTT
from stt.speech_module.main import SpeechSTT
from stt.telegram.main import TelegramMessenger

if data['stt'] == 'google':
    stt_engine = GoogleSTT()
elif data['stt'] == 'speech':
    stt_engine = SpeechSTT()
elif data['stt'] == 'sphinx':
    stt_engine = SphinxSTT(
        modeldir=data['modeldir'], hmm=data['hmm'],
        lm=data['lm'], dic=data['dic']
    )
elif data['stt'] == 'watson':
    stt_engine = WatsonSTT(username=data['watson_username'],
                           password=data['watson_password'])
elif data['stt'] == 'telegram':
    stt_engine = TelegramMessenger()
while True:
    if data['stt'] == 'telegram':
        stt_engine.send()
    else:
        text = ''  # Text returned by STT Engine
    # tts_engine.speak(text)  User's query
    response = ''  # Response given by actions corresponding to text
    # tts_engine.speak(response)  # TTS Engine gives the response
    print(response)
