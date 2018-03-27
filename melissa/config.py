# Melissa
from profile import data
from stt.speech_recognition_module.googleSTT import GoogleSTT
from stt.speech_recognition_module.sphinxSTT import SphinxSTT
from stt.watson.main import WatsonSTT
from stt.speech_module.main import SpeechSTT

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

text = stt_engine.write()
"""
stt_engine.write() is responsible for Speech to text which
returns the text to variable text

"""
