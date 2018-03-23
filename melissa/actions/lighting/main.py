import subprocess

# Melissa

WORDS = {'very_dark': {'groups': ['dark']},
         'feeling_angry': {'groups': [['feeling', 'angry']]},
         'feeling_creative': {'groups': [['feeling', 'creative']]},
         'feeling_lazy': {'groups': [['feeling', 'lazy']]},
         'turn_off': {'groups': [['lights', 'off']]}}


class Lighting():

    def very_dark(self, text):
        subprocess.call(['blink1-tool', '--white'])
        return 'Better now?'

    def feeling_angry(self, text):
        subprocess.call(['blink1-tool', '--cyan'])
        return 'Calm down dear!'

    def feeling_creative(self, text):
        subprocess.call(['blink1-tool', '--magenta'])
        return 'So good to hear that!'

    def feeling_lazy(self, text):
        subprocess.call(['blink1-tool', '--yellow'])
        return 'Rise and shine dear!'

    def turn_off(self, text):
        subprocess.call(['blink1-tool', '--off'])
        return "Lights Off"
