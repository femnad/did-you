#!/usr/bin/env python2
import gevent
import zmq.green as zmq
from did_you_pb2 import TaskCommand, Task, TaskList

class TaskServer(object):

    def __init__(self):
        self._tasks = set()

    def print_tasks(self):
        if len(self._tasks) == 0:
            print('No tasks')
        else:
            print('Incomplete Tasks')
            for item_no, task in enumerate(self._tasks, 1):
                print("{}: {}".format(item_no, task))

    def serve(self):
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://*:5555")

        while True:
            message = socket.recv()
            task_command = TaskCommand()
            task_command = task_command.FromString(message)
            if TaskCommand.Command.Name(task_command.command) == 'DO':
                self._tasks.add(task_command.task.name)
                socket.send(b"Ack")
            elif TaskCommand.Command.Name(task_command.command) == 'DONE':
                task = task_command.task
                if task.name in self._tasks:
                    self._tasks.remove(task_command.task.name)
                socket.send(b"Ack")
            elif TaskCommand.Command.Name(task_command.command) == 'LIST':
                task_list = TaskList()
                for task_name in self._tasks:
                    task = task_list.tasks.add()
                    task.name = task_name
                socket.send(task_list.SerializeToString())
            else:
                print("Unknown command:")
            self.print_tasks()

if __name__ == "__main__":
    task_server = TaskServer()
    task_serving = gevent.spawn(task_server.serve)
    gevent.joinall([task_serving])
