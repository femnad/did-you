# Package: did_you_server.command
import os.path
import threading

from did_you.config import DidYouConfig
from did_you.utils import cmdline_args
from did_you.server import TaskServer

DEFAULT_CONFIG_FILE = "~/.did_you.conf"

@cmdline_args
def run_server(config_file):
    if config_file is None:
        config_file = DEFAULT_CONFIG_FILE
    if config_file.startswith('~'):
        config_file = os.path.expanduser(config_file)
    configurator = DidYouConfig(config_file)
    task_server = TaskServer(configurator)
    responder = threading.Thread(target=task_server.respond)
    responder.start()
    publisher = threading.Thread(target=task_server.publish)
    publisher.start()
