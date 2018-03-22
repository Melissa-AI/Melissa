import os
from melissa.profile import data
import speech_recognition as sr
from melissa.stt_facade import STT
try:
    from pocketsphinx.pocketsphinx import *
    from sphinxbase.sphinxbase import *
except:
    pass


class SphinxSTT(STT):

    def __init__(self):
        self.r = sr.Recognizer()
        self.modeldir = data['pocketsphinx']['modeldir']
        self.hmm = data['pocketsphinx']['hmm']
        self.lm = data['pocketsphinx']['lm']
        self.dic = data['pocketsphinx']['dic']
        self.config = Decoder.default_config()

    def write(self):
        while True:
            self.config.set_string('-hmm', os.path.join(modeldir, hmm))
            self.config.set_string('-lm', os.path.join(modeldir, lm))
            self.config.set_string('-dict', os.path.join(modeldir, dic))
            self.config.set_string('-logfn', '/dev/null')
            self.decoder = Decoder(self.config)

            stream = open('recording.wav', 'rb')
            in_speech_bf = False
            self.decoder.start_utt()
            while True:
                buf = stream.read(1024)
                if buf:
                    self.decoder.process_raw(buf, False, False)
                    if self.decoder.get_in_speech() != in_speech_bf:
                        in_speech_bf = self.decoder.get_in_speech()
                        if not in_speech_bf:
                             self.decoder.end_utt()
                             speech_text = self.decoder.hyp().hypstr
                             print speech_text
                             self.decoder.start_utt()
                 else:
                     break
             decoder.end_utt()
             return speech_text.lower().replace("'", "")

