#!/usr/bin/env python3
import capnp
import sys
import taskdef_capnp
import zmq

from did_you_config import DidYouConfig


class TaskCommander(object):

    def __init__(self):
        context = zmq.Context()
        self._socket = context.socket(zmq.REQ)
        configurator = DidYouConfig()
        host = configurator.host
        port = configurator.request_port
        self._socket.connect("tcp://{}:{}".format(host, port))

    def run_command(self, command, task_name):
        task = taskdef_capnp.Task.new_message()
        task.name = task_name
        task_message = taskdef_capnp.TaskMessage.new_message()
        task_message.task = task
        task_message.command = command
        self._socket.send(task_message.to_bytes())
        return self._socket.recv()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        executable_name = sys.argv[0]
        print("Usage {} <command> <task-name>".format(executable_name))
        exit()
    command, task_name = sys.argv[1:]
    task_commander = TaskCommander()
    try:
        response = task_commander.run_command(command, task_name)
        print("Got response: {}".format(str(response, 'UTF-8')))
    except AttributeError:
        print("No such command: {}".format(command))
