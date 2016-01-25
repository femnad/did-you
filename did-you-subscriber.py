#!/usr/bin/env python2
import gevent
import zmq.green as zmq

class TaskSubscriber(object):

    def __init__(self):
        context = zmq.Context()
        self._socket = context.socket(zmq.SUB)
        self._socket.connect("tcp://localhost:5556")

    def get_task_list(self):
        message = self._socket.recv()
        print(message)

if __name__ == "__main__":
    task_subscriber = TaskSubscriber()
    subscription = gevent.spawn(task_subscriber.get_task_list)
    gevent.joinall([subscription])
    
