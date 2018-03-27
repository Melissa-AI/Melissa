import speech
from melissa.stt import STT


class SpeechSTT(STT):

    def __init__(self):
        self.name = 'speech'

    def write(self):
        print "Talk:"
        phrase = speech.input()
        speech.say("%s" % phrase)
        return phrase
