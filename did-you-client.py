#!/usr/bin/env python2
import gevent
import sys
import zmq.green as zmq
from did_you_pb2 import TaskCommand, Task, TaskList

class TaskCommander(object):

    def __init__(self):
        context = zmq.Context()
        self._socket = context.socket(zmq.REQ)
        self._socket.connect("tcp://localhost:5555")

    def run_command(self, command, task_name):
        if command.upper() not in TaskCommand.Command.keys():
            return
        task_command = TaskCommand()
        task_command.command = TaskCommand.Command.Value(command.upper())
        task_command.task.name = task_name
        self._socket.send(task_command.SerializeToString())
        message = self._socket.recv()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        executable_name = sys.argv[0]
        print("Usage {} <command> <task-name>".format(executable_name))
        exit()
    command, task_name = sys.argv[1:]
    task_commander = TaskCommander()
    request = gevent.spawn(task_commander.run_command, command, task_name)
    gevent.joinall([request])
