# Package: did_you_server.command
import os.path
import threading

from did_you.server import TaskServer
from did_you.config import DidYouConfig

def run_server():
    config_file = os.path.expanduser("~/.did_you.conf")
    configurator = DidYouConfig(config_file)
    task_server = TaskServer(configurator)
    responder = threading.Thread(target=task_server.respond)
    responder.start()
    publisher = threading.Thread(target=task_server.publish)
    publisher.start()
