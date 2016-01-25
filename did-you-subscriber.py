#!/usr/bin/env python2
import gevent
import zmq.green as zmq
from did_you_pb2 import TaskList

class TaskSubscriber(object):

    def __init__(self):
        context = zmq.Context()
        self._socket = context.socket(zmq.SUB)
        self._socket.connect("tcp://localhost:5556")
        self._socket.setsockopt(zmq.SUBSCRIBE, b'')

    def get_task_list(self):
        message = self._socket.recv()
        task_list = TaskList()
        task_list = task_list.FromString(message)
        for task in task_list.tasks:
            print(task.name)

if __name__ == "__main__":
    task_subscriber = TaskSubscriber()
    subscription = gevent.spawn(task_subscriber.get_task_list)
    gevent.joinall([subscription])
    
