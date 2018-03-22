from melissa.profile import data
import speech_recognition as sr
from melissa.stt_facade import STT

class GoogleSTT(STT):

    def __init__(self):
        self.r = sr.Recognizer()

    def write(self):
        while True:
            with sr.Microphone() as source:
                self.r.adjust_for_ambient_noise(source)
                print("Say something!")
                audio = r.listen(source)
            try:
                speech_text = self.r.recognize_google(audio).lower().replace("'", "")
                print("Melissa thinks you said '" + speech_text + "'")
                return speech_text
            except sr.UnknownValueError:
                print("Melissa could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
            else:
                pass


