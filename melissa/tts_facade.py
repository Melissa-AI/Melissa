import sys
import subprocess

import pyvona

# Melissa
import profile

class TTS(object):

    def speak(self, message):
    """
    This function takes a message as an argument and converts it to
    speech depending on the OS.
    """
        raise NotImplementedError()

