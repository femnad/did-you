# Package: did_you_server.command
import os.path
import sys
import threading

from did_you.config import DidYouConfig
from did_you.server import TaskServer

DEFAULT_CONFIG_FILE = "~/.did_you.conf"

def run_server():
    arguments = sys.argv[1:]
    if len(arguments) == 0:
        config_file = DEFAULT_CONFIG_FILE
    else:
        config_file = arguments[0]
    if config_file.startswith('~'):
        config_file = os.path.expanduser(config_file)
    configurator = DidYouConfig(config_file)
    task_server = TaskServer(configurator)
    responder = threading.Thread(target=task_server.respond)
    responder.start()
    publisher = threading.Thread(target=task_server.publish)
    publisher.start()
