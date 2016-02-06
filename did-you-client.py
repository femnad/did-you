#!/usr/bin/env python3
import msgpack
import sys
import zmq

from did_you_config import DidYouConfig
from task_command import TaskCommand


class TaskCommander(object):

    def __init__(self):
        context = zmq.Context()
        self._socket = context.socket(zmq.REQ)
        configurator = DidYouConfig()
        host = configurator.host
        port = configurator.request_port
        self._socket.connect("tcp://{}:{}".format(host, port))

    def run_command(self, command, task_name):
        task_message = {"name": task_name, "command": command.value}
        self._socket.send(msgpack.packb(task_message))
        return self._socket.recv()

class TaskSubscriber(object):

    def __init__(self):
        configurator = DidYouConfig()
        host = configurator.host
        port = configurator.subscription_port
        context = zmq.Context()
        self._socket = context.socket(zmq.SUB)
        self._socket.connect("tcp://{}:{}".format(host, port))
        self._socket.setsockopt(zmq.SUBSCRIBE, b'')

    def get_task_list(self):
        task_list = msgpack.unpackb(self._socket.recv())
        for task in task_list:
            print(task)

if __name__ == "__main__":
    if not 2 <= len(sys.argv) <= 3:
        executable_name = sys.argv[0]
        print("Usage {} <command> [<task-name>]".format(executable_name))
        exit()
    command = sys.argv[1]
    if command == 'list':
        task_subscriber = TaskSubscriber()
        task_subscriber.get_task_list()
    else:
        task_name = sys.argv[2]
        task_commander = TaskCommander()
        try:
            response = task_commander.run_command(
                TaskCommand[command], task_name)
            print("Got response: {}".format(str(response, 'UTF-8')))
        except AttributeError:
            print("No such command: {}".format(command))
