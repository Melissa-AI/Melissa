# Melissa
from profile import data
import sys
from tts import TTS
import importlib
import pkgutil
import inspect

dict_tts = dict()
for (_, name, _) in pkgutil.iter_modules(["tts_engines"]):
    module = importlib.import_module('.' + name + ".main", "tts_engines")
    for cls, obj in inspect.getmembers(module):
        if obj in TTS.__subclasses__():
            class_ = getattr(module, cls)
            dict_tts[str(class_.name)] = class_
print(dict_tts)
try:
    if data['tts'] in dict_tts.keys():
        tts_engine = dict_tts[data['tts']]
except KeyError as e:
    print(dict_tts.keys())
    sys.exit(0)

while True:
    text = ''  # Text returned by STT Engine

    tts_engine.speak(text)  # User's query

    response = ''  # Response given by actions corresponding to text

    tts_engine.speak(response)  # TTS Engine gives the response
    print(response)

