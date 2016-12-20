import re
import wikipedia

# Melissa
from melissa.tts import tts

WORDS = {'define_define': {'groups': ['define']},
		'define_whatis': {'groups': ['what', 'is']},
		'define_whats': {'groups': ['whats']}
         }
def define_define(speech_text):
    words_of_message = speech_text.split()
    words_of_message.remove('define')
    define_subject(words_of_message)

def define_whatis(speech_text):
    words_of_message = speech_text.split()
    words_of_message.remove('what')
    words_of_message.remove('is')
    define_subject(words_of_message)

def define_whats(speech_text):
    words_of_message = speech_text.split()
    words_of_message.remove('whats')
    define_subject(words_of_message)

def define_subject(words_of_message):
    cleaned_message = ' '.join(words_of_message).rstrip()
    if len(cleaned_message) == 0:
        msg = 'define requires subject words'
        print msg
        tts(msg)
        return

    try:
        wiki_data = wikipedia.summary(cleaned_message, sentences=5)

        regEx = re.compile(r'([^\(]*)\([^\)]*\) *(.*)')
        m = regEx.match(wiki_data)
        while m:
            wiki_data = m.group(1) + m.group(2)
            m = regEx.match(wiki_data)

        wiki_data = wiki_data.replace("'", "")
        tts(wiki_data)
    except wikipedia.exceptions.DisambiguationError as e:
        tts('Can you please be more specific? You may choose something' +
            'from the following.')
        print("Can you please be more specific? You may choose something" +
              "from the following; {0}".format(e))
