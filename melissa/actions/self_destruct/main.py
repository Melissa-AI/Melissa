import subprocess

# Melissa

WORDS = {'self_destruct': {'groups': [['self', 'destruct']]}}


class SelfDestruct():

    def self_destruct(self, text):
        subprocess.call(['sudo', 'rm', '-r', '../Melissa-Core'])
        quit()
        return 'Self destruction mode engaged, over and out.'
