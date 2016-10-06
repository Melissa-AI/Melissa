from datetime import datetime
import calendar

# Melissa
from melissa.tts import tts

WORDS = {
  'what_is_time': {'groups': ['time']}
  'what_is_date': {'groups': ['date']}
  'what_is_day': {'groups': ['day']}
}

def what_is_time(text):
    tts("The time is " + datetime.strftime(datetime.now(), '%H:%M:%S'))
    
def what_is_date(text):
    my_date = date.today()
    tts("Today's day is" + calendar.day_name[my_date.weekday()])
    
def what_is_time(text):
    tts("Today's date is" + datetime.now().strftime('%Y-%m-%d'))
