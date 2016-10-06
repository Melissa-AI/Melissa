# Melissa
from melissa.tts import tts


WORDS = {'repeat_text': {'groups': ['spell']}}


def repeat_text(text):
    text = text.split(' ', 1)[1]
    tts(text)
