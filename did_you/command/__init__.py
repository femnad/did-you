# Package: did_you_server.command
import os
import os.path
import sys
import threading

from did_you.config import DidYouConfig
from did_you.server import TaskServer
from did_you.utils import parse_arguments

DEFAULT_CONFIG_FILE = "~/.did_you.conf"
DEFAULT_PID_FILE = "/tmp/did_you.pid"


def run_server():
    config_file, pid_file = parse_arguments(
        sys.argv, ['config_file', 'pid_file'])
    if config_file is None:
        config_file = DEFAULT_CONFIG_FILE
    if pid_file is None:
        pid_file = DEFAULT_PID_FILE
    if config_file.startswith('~'):
        config_file = os.path.expanduser(config_file)
    pid = os.getpid()
    with open(pid_file, 'w') as pid_file_descriptor:
        pid_file_descriptor.write("{}\n".format(pid))
    configurator = DidYouConfig(config_file)
    task_server = TaskServer(configurator)
    responder = threading.Thread(target=task_server.respond)
    responder.start()
    publisher = threading.Thread(target=task_server.publish)
    publisher.start()
