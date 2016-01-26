#!/usr/bin/env python3
import zmq

class TaskSubscriber(object):

    def __init__(self):
        context = zmq.Context()
        self._socket = context.socket(zmq.SUB)
        self._socket.connect("tcp://localhost:5556")
        self._socket.setsockopt(zmq.SUBSCRIBE, b'')

    def get_task_list(self):
        message = str(self._socket.recv(), 'utf-8')
        for task in message.split():
            print(task)

if __name__ == "__main__":
    ts = TaskSubscriber()
    ts.get_task_list()
