# Melissa
from profile import data
import importlib
import pkgutil
import importlib
import inspect

dict_tts = dict()
for (_, name, _) in pkgutil.iter_modules(["tts_engines"]):
    module = importlib.import_module('.' + name + ".main", "tts_engines")
    
    for cls, obj in inspect.getmembers(module):
        if inspect.isclass(obj):
            class_ = getattr(module,cls)
            attributes = inspect.getmembers(class_)
            li = [a for a in attributes if not(a[0].startswith('__') and a[0].endswith('__'))]
            engine_name = li[0][1]
            dict_tts[engine_name] = cls
print(dict_tts)

if data['tts'] in dict_tts.keys():
    tts_engine = dict_tts[data['tts']]

while True:
    text = ''  # Text returned by STT Engine

    tts_engine.speak(text)  # User's query

    response = ''  # Response given by actions corresponding to text

    tts_engine.speak(response)  # TTS Engine gives the response
    print(response)

