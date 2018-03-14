import re
import wikipedia

# Melissa
from melissa.config import tts_engine


class Subject(object):

    WORDS = {'define_subject': {'groups': ['define']}}

    def define_subject(self, speech_text):
        words_of_message = speech_text.split()
        words_of_message.remove('define')
        cleaned_message = ' '.join(words_of_message).rstrip()
        if len(cleaned_message) == 0:
            msg = 'define requires subject words'
            print msg
            tts_engine.speak(msg)
            return

        try:
            wiki_data = wikipedia.summary(cleaned_message, sentences=5)

            regEx = re.compile(r'([^\(]*)\([^\)]*\) *(.*)')
            m = regEx.match(wiki_data)
            while m:
                wiki_data = m.group(1) + m.group(2)
                m = regEx.match(wiki_data)

            wiki_data = wiki_data.replace("'", "")
            tts_engine.speak(wiki_data)
        except wikipedia.exceptions.DisambiguationError as e:
            return(
                'Can you please be more specific? You may choose something' +
                'from the following.'
            )
            print("Can you please be more specific? You may choose something" +
                  "from the following; {0}".format(e))
