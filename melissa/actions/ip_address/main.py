import re

from netifaces import interfaces, ifaddresses, AF_INET

# Melissa

WORDS = {
    'ip_address': {
        'groups': [
            'ip', ['ip', 'address'], ['network', 'address']
        ]
    }
}


class IpAddress():

    def ip_address(self, text):
        for ifaceName in interfaces():
            addresses = [
                i['addr'] for i in
                ifaddresses(ifaceName).setdefault(
                    AF_INET, [{'addr': None}])]
            if None in addresses:
                addresses.remove(None)
            if addresses and ifaceName != "lo":
                updated_addresses = [re.sub(r"\.", r" dot ", address)
                                     for address in addresses]
                return(
                    '%s: %s' % (
                        "interface: " + ifaceName +
                        ", I.P. Address ", ', '.join(updated_addresses)
                    )
                )
