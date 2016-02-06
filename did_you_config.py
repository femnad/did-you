import configparser


class DidYouConfig(object):

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('did_you.conf')
        self._default_section = config['default']
        self._redis_section = config['redis']
        self._task_checker_section = config['task_checker']

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
    def redis_port(self):
        return self._redis_section['port']

    @property
    def sleep_period(self):
        return self._task_checker_section['sleep_period']
