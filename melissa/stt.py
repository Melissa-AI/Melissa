# Inspired by stt from the Jasper project http://jasperproject.github.io/

import os
import speech_recognition as sr
from abc import ABCMeta, abstractmethod

# Melissa
import profile

if profile.data['stt'] == 'sphinx':
    try:
        from pocketsphinx.pocketsphinx import *
        from sphinxbase.sphinxbase import *
    except:
        print 'Error: Could not import pocketsphinx'
        quit()


class base_stt(object):
    """
    Generic base class for all STT engines
    """

    __metaclass__ = ABCMeta

    @classmethod
    def get_instance(cls):
        return cls()

    @abstractmethod
    def transcribe(self):
        pass


class pocketsphinx_stt(base_stt):
    """
    """

    NAME = 'sphinx'

    def __init__(self):

        """
        Initiates the pocketsphinx instance.
        """
        self.r = sr.Recognizer()
        modeldir = profile.data['pocketsphinx']['modeldir']
        hmm = profile.data['pocketsphinx']['hmm']
        lm = profile.data['pocketsphinx']['lm']
        dic = profile.data['pocketsphinx']['dic']

        config = Decoder.default_config()
        config.set_string('-hmm', os.path.join(modeldir, hmm))
        config.set_string('-lm', os.path.join(modeldir, lm))
        config.set_string('-dict', os.path.join(modeldir, dic))
        config.set_string('-logfn', '/dev/null')
        self.decoder = Decoder(config)

    def decode(self):
        stream = open('recording.wav', 'rb')
        stream.seek(44) # bypasses wav header

        data = stream.read()
        self.decoder.start_utt()
        self.decoder.process_raw(data, False, True)
        self.decoder.end_utt()

        speech_text = self.decoder.hyp().hypstr
        print(profile.data['va_name'] + " thinks you said '"
              + speech_text + "'")
        return speech_text.lower().replace("'", "")

    def transcribe(self):
        with sr.Microphone() as source:
            self.r.adjust_for_ambient_noise(source)
            print("Say something!")
            audio = self.r.listen(source)

        with open("recording.wav", "wb") as f:
            f.write(audio.get_wav_data())

        return self.decode()


class google_stt(base_stt):
    """
    Google Speech-To-Text implementation.
    """

    NAME = 'google'

    def __init__(self):
        self.r = sr.Recognizer()

    def transcribe(self):
        with sr.Microphone() as source:
            self.r.adjust_for_ambient_noise(source)
            print("Say something!")
            audio = self.r.listen(source)

        try:
            speech_text = self.r.recognize_google(audio).lower().replace("'", "")
            print(profile.data['va_name'] + " thinks you said '"
                  + speech_text + "'")

        except sr.UnknownValueError:
            print(profile.data['va_name']
                  + " could not understand audio")

        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

        else:
            return speech_text


def get_engine_by_name(name=None):
    """
    Select an STT engine (class) using the NAME attribute in the STT
    classes.
    """

    if not name or type(name) is not str:
        raise TypeError("Invalid STT name '%s'", name)

    selected_engines = filter(lambda engine: hasattr(engine, "NAME") and
                              engine.NAME == name, get_engines())

    if len(selected_engines) == 0:
        raise ValueError("No STT engine found for name '%s'" % name)
    else:
        if len(selected_engines) > 1:
            print(("WARNING: Multiple STT engines found for name '%s'. " +
                   "This is most certainly a bug.") % name)

        return selected_engines[0]


def get_engines():
    def get_subclasses(cls):
        subclasses = set()
        for subclass in cls.__subclasses__():
            subclasses.add(subclass)
        return subclasses

    return [stt_engine for stt_engine in
            list(get_subclasses(base_stt))
            if hasattr(stt_engine, 'NAME') and stt_engine.NAME]

