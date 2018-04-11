from melissa.stt import STT
from melissa.profile import data
from melissa import brain
import telepot
import time


class TelegramMessenger(STT):

    name = 'telegram'

    def handle(self, msg):
        username = msg['chat']['username']
        command = msg['text'].lower().replace("'", "")
        if username == data['telegram_username']:
            print(data['va_name'] + " thinks you said '" + command + "'")
            brain.query(command)

    def write(self):
        while True:
            if data['telegram_token'] == '':
                quit()
            else:
                bot = telepot.Bot(data['telegram_token'])
                bot.notifyOnMessage(self.handle)
                while 1:
                    time.sleep(10)
