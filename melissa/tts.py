class TTS(object):

    def __init__(self):
    self.name = ''
    
    def speak(self, message):
        """
        This function takes a message as an argument and converts it to
        speech depending on the OS.
        """
        raise NotImplementedError()
