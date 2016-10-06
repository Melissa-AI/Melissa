from datetime import datetime
import time
import datetime

# Melissa
from melissa.tts import tts

WORDS = {'what_is_time': {'groups': ['time']}}
WORDS = {'what_is_date': {'groups': ['date']}}
WORDS = {'what_is_day': {'groups': ['day']}}


def what_is_time(text):
    now = datetime.datetime.now()
    print("The time is " + now.strftime('%H:%M:%S'))
def what_is_date(text):
    print("The date is " + time.strftime("%d/%m/%Y"))
def what_is_day(text):
    now = datetime.datetime.now()
    print("The day is " + now.strftime("%A"))

