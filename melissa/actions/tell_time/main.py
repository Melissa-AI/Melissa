from datetime import datetime

# Melissa

WORDS = {
    'what_is_time': {'groups': ['time']},
    'what_is_date': {'groups': ['date']},
    'what_is_day': {'groups': ['day']}
}


class TellTime():

    def what_is_time(self, text):
        return("The time is " + datetime.strftime(datetime.now(), '%H:%M:%S'))

    def what_is_date(self, text):
        return("The date is " + datetime.strftime(datetime.now(), '%m/%d/%Y'))

    def what_is_day(self, text):
        return("The day is " + datetime.strftime(datetime.now(), '%A'))
