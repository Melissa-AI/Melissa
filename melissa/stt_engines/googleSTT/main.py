import speech_recognition as sr
from melissa.stt import STT


class GoogleSTT(STT):

    name = 'google'

    def write(self):

        self.r = sr.Recognizer()
        while True:
            with sr.Microphone() as source:
                self.r.adjust_for_ambient_noise(source)
                audio = self.r.listen(source)
            try:
                speech_text = self.r.recognize_google(audio).lower().replace(
                    "'", ""
                )
                return speech_text
            except sr.UnknownValueError:
                return "Melissa could not understand audio"
            except sr.RequestError as e:
                return(
                    "Could not request results from Google "
                    "Speech {0}".format(e)
                )
