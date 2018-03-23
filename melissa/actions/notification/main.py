from melissa.profile import data
from pushbullet import Pushbullet


def handle_exceptions(f):  # pragma: no cover
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            print("Error: ", e)
    return inner


class Notifications():

    @handle_exceptions
    def push(self, info):
        pb = Pushbullet(data['push_bullet'])
        pb.push_note(data['va_name'], info)  # Send Notification
