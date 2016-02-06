import configparser


class DidYouConfig(object):

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('did_you.conf')
        self._default_section = config['default']
        self._redis_section = config['redis']

    @property
    def request_port(self):
        return self._default_section['request_port']

    @property
    def subscription_port(self):
        return self._default_section['subscription_port']

    @property
    def host(self):
        return self._default_section['host']

    @property
    def redis_host(self):
        return self._redis_section['host']

    @property
    def redist_port(self):
        return self._redis_section['port']
