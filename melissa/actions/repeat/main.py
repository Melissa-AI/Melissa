# Melissa
WORDS = {'repeat_text': {'groups': ['repeat', 'say']}}


class Repeat():

    def repeat_text(self, text):
        text = text.split(' ', 1)[1]
        return text
