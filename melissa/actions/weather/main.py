import pywapi

# Melissa
from melissa.profile import data

WORDS = {'weather': {'groups': ['weather', ['how', 'weather'],
                                ['hows', 'weather']]}}


class Weather():

    def weather(self, text):
        weather_com_result = pywapi.get_weather_from_weather_com(
            data['city_code']
        )

        current_conditions = weather_com_result['current_conditions']
        temperature = float(current_conditions['temperature'])
        degrees_type = 'celcius'

        if data['degrees'] == 'fahrenheit':
            temperature = (temperature * 9 / 5) + 32
            degrees_type = 'fahrenheit'

        weather_result = "Weather.com says: It is " + \
            weather_com_result['current_conditions']['text'].lower() + \
            " and " + str(temperature) + "degrees " + degrees_type + \
            " now in " + data['city_name']
        return weather_result
