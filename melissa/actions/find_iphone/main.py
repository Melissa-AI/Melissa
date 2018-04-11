from pyicloud import PyiCloudService
from pyicloud.exceptions import PyiCloudFailedLoginException

# Melissa
from melissa import profile
from melissa.config import tts_engine

WORDS = {'find_iphone': {'groups': [['find', 'iphone'], [
    'ring', 'iphone']]}, 'iphone_battery': {'groups': [['battery', 'iphone']]}}

ICLOUD_USERNAME = profile.data['icloud']['username']
ICLOUD_PASSWORD = profile.data['icloud']['password']


class IPhone(object):

    def find_iphone(self, text):
        try:
            api = PyiCloudService(ICLOUD_USERNAME, ICLOUD_PASSWORD)
        except PyiCloudFailedLoginException:
            tts_engine.speak("Invalid Username & Password")
        return

        # All Devices
        devices = api.devices

        # Just the iPhones
        iphones = []

        for device in devices:
            current = device.status()
            if "iPhone" in current['deviceDisplayName']:
                iphones.append(device)

        # The one to ring
        phone_to_ring = None

        if len(iphones) == 0:
            return "No iPhones found in your account"

        elif len(iphones) == 1:
            phone_to_ring = iphones[0]
            phone_to_ring.play_sound()
            return "Sending ring command to the phone now"

        elif len(iphones) > 1:
            for phone in iphones:
                phone_to_ring = phone
                phone_to_ring.play_sound()
                return "Sending ring command to the phone now"

    def iphone_battery(self, text):
        try:
            api = PyiCloudService(ICLOUD_USERNAME, ICLOUD_PASSWORD)
        except PyiCloudFailedLoginException:
            return "Invalid Username & Password"
            return

        # All Devices
        devices = api.devices

        # Just the iPhones
        iphones = []

        for device in devices:
            current = device.status()
            if "iPhone" in current['deviceDisplayName']:
                iphones.append(device)

        for phone in iphones:
            status = phone.status()
            battery = str(int(float(status['batteryLevel']) * 100))
            return(
                battery + 'percent battery left in ' + status['name']
            )
