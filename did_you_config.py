import configparser


class DidYouConfig(object):

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('did_you.conf')
        self._default_section = config['Default']

    @property
    def request_port(self):
        return self._default_section['RequestPort']

    @property
    def subscription_port(self):
        return self._default_section['SubscriptionPort']

    @property
    def host(self):
        return self._default_section['Host']
