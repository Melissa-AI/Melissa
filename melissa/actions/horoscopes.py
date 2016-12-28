from horoscope import Horoscope
from melissa import profile

# Melissa
from melissa.tts import tts

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


def tell_horoscope(text):
    today_horoscope = Horoscope.get_todays_horoscope(profile.data['sun_sign'])
    tts(today_horoscope['horoscope'])
