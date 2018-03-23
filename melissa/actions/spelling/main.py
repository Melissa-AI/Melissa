# Melissa
WORDS = {'spell_text': {'groups': ['spell']}}


class Spelling():

    def spell_text(self, text):
        text = list(text.split(' ', 1)[1])
        spelling = ' '.join(text)
        return spelling
