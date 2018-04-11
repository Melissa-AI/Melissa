import speech
from melissa.stt import STT


class SpeechSTT(STT):

    name = 'win_speech'

    def write(self):
        phrase = speech.input()
        speech.say("%s" % phrase)
        return phrase
