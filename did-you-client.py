#!/usr/bin/env python2
import sys
import zmq
from did_you_pb2 import TaskCommand, Task, TaskList

context = zmq.Context()

socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

if len(sys.argv) < 2:
    executable_name = sys.argv[0]
    print("Usage: {} <command> [<task>]".format(executable_name))
    exit()
else:
    command = sys.argv[1]
    if command.upper() not in TaskCommand.Command.keys():
        print("Unknown command: {}".format(command))
        exit()
    task_command = TaskCommand()
    task_command.command = TaskCommand.Command.Value(command.upper())
    if len(sys.argv) == 3:
        task_name = sys.argv[2]
        task_command.task.name = task_name
    socket.send(task_command.SerializeToString())
    message = socket.recv()
    if len(sys.argv) == 2 and command.upper() == 'LIST':
        task_list = TaskList.FromString(message)
        for task in task_list.tasks:
            print(task.name)
    else:
        print(message)
