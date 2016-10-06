from datetime import datetime
import time
import datetime

# Melissa
from melissa.tts import tts

WORDS = {'what_is_time': {'groups': ['time']}}
WORDS = {'what_is_date': {'groups': ['date']}}
WORDS = {'what_is_day': {'groups': ['day']}}



def what_is_time(text):
    tts("The time is " + datetime.strftime(datetime.now(), '%H:%M:%S'))
def what_is_date(text):
    tts("The date is " + time.strftime("%d/%m/%Y"))
def what_is_day(text):
    tts("The day is " + now.strftime("%A"))
