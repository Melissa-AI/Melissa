import os
from melissa.stt import STT
from pocketsphinx import Decoder
from melissa.profile import data


class SphinxSTT(STT):

    name = 'sphinx'
    modeldir = data['modeldir']
    hmm = data['hmm']
    lm = data['lm']
    dic = data['dic']
    config = Decoder.default_config()

    def write(self):
        self.config.set_string(
            '-hmm', os.path.join(self.modeldir, self.hmm)
        )
        self.config.set_string(
            '-lm', os.path.join(self.modeldir, self.lm)
        )
        self.config.set_string(
            '-dict', os.path.join(self.modeldir, self.dic)
        )
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
        self.decoder.end_utt()
        return speech_text.lower().replace("'", "")
