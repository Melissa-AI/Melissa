from horoscope_generator import HoroscopeGenerator

# Melissa

WORDS = {
    'tell_horoscope': {
        'groups': [
            ['tell', 'future'],
            ['say', 'wise'],
            ['how', 'day'],
            ['hows', 'day'],
            ['how', 'today'],
            ['hows', 'today'],
            'horoscope'
        ]
    }
}


class Horoscope():

    def tell_horoscope(self, text):
        return HoroscopeGenerator.format_sentence(
            HoroscopeGenerator.get_sentence()
        )
