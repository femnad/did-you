#!/usr/bin/env python3
import capnp
import taskdef_capnp
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
        task_list = taskdef_capnp.TaskList.from_bytes(self._socket.recv())
        for task in task_list.tasks:
            print(task.name)

if __name__ == "__main__":
    task_subscriber = TaskSubscriber()
    task_subscriber.get_task_list()
