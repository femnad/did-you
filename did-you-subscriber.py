#!/usr/bin/env python3
import msgpack
import zmq

from did_you_config import DidYouConfig


class TaskSubscriber(object):

    def __init__(self):
        configurator = DidYouConfig()
        host = configurator.host
        port = configurator.subscription_port
        context = zmq.Context()
        self._socket = context.socket(zmq.SUB)
        self._socket.connect("tcp://{}:{}".format(host, port))
        self._socket.setsockopt(zmq.SUBSCRIBE, b'')

    def get_task_list(self):
        task_list = msgpack.unpackb(self._socket.recv())
        for task in task_list:
            print(task)

if __name__ == "__main__":
    task_subscriber = TaskSubscriber()
    task_subscriber.get_task_list()
