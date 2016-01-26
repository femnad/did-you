#!/usr/bin/env python3
import sys
import zmq


class NoSuchCommandException(Exception):

    def __init__(self, command):
        self.command = command


class TaskCommander(object):

    def __init__(self):
        context = zmq.Context()
        self._socket = context.socket(zmq.REQ)
        self._socket.connect("tcp://localhost:5555")

    def run_command(self, task_command):
        self._socket.send(task_command)
        print(self._socket.recv())

if __name__ == "__main__":
    if len(sys.argv) != 3:
        executable_name = sys.argv[0]
        print("Usage {} <command> <task-name>".format(executable_name))
        exit()
    command, task_name = sys.argv[1:]
    task_commander = TaskCommander()
    task_commander.run_command(':'.join([command, task_name]))
