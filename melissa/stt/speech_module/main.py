import speech
from melissa.stt_facade import STT


class SpeechSTT(STT):

    def write(self):
        print "Talk:"
        phrase = speech.input()
        speech.say("You said %s" % phrase)
        return "You said {0}".format(phrase)
