#!/usr/bin/env python2
import zmq
from did_you_pb2 import TaskCommand, Task, TaskList

def print_tasks(task_list):
    if len(task_list) == 0:
        print('No tasks')
    else:
        print('Incomplete Tasks')
        for item_no, task in enumerate(task_list, 1):
            print("{}: {}".format(item_no, task))

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
tasks = set()

while True:
    message = socket.recv()
    task_command = TaskCommand()
    task_command = task_command.FromString(message)
    if TaskCommand.Command.Name(task_command.command) == 'DO':
        tasks.add(task_command.task.name)
        socket.send(b"Ack")
    elif TaskCommand.Command.Name(task_command.command) == 'DONE':
        task = task_command.task
        if task.name in tasks:
            tasks.remove(task_command.task.name)
        socket.send(b"Ack")
    elif TaskCommand.Command.Name(task_command.command) == 'LIST':
        task_list = TaskList()
        for task_name in tasks:
            task = task_list.tasks.add()
            task.name = task_name
        socket.send(task_list.SerializeToString())
    else:
        print("Unknown command:")
    print_tasks(tasks)
