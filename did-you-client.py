#!/usr/bin/env python3
import sys
import capnp
import taskdef_capnp
import zmq


class NoSuchCommandException(Exception):

    def __init__(self, command):
        self.command = command


class TaskCommander(object):

    def __init__(self):
        context = zmq.Context()
        self._socket = context.socket(zmq.REQ)
        self._socket.connect("tcp://localhost:5555")

    def run_command(self, command, task_name):
        task = taskdef_capnp.Task.new_message()
        task.name = task_name
        task_message = taskdef_capnp.TaskMessage.new_message()
        task_message.task = task
        task_message.command = command
        self._socket.send(task_message.to_bytes())
        print(self._socket.recv())

if __name__ == "__main__":
    if len(sys.argv) != 3:
        executable_name = sys.argv[0]
        print("Usage {} <command> <task-name>".format(executable_name))
        exit()
    command, task_name = sys.argv[1:]
    task_commander = TaskCommander()
    task_commander.run_command(command, task_name)
