#!/usr/bin/env python3
import capnp
import taskdef_capnp
import zmq

class TaskSubscriber(object):

    subscription_host = 'localhost'
    subscription_port = 5556

    def __init__(self):
        context = zmq.Context()
        self._socket = context.socket(zmq.SUB)
        self._socket.connect("tcp://{}:{}".format(
            self.subscription_host, self.subscription_port))
        self._socket.setsockopt(zmq.SUBSCRIBE, b'')

    def get_task_list(self):
        task_list = taskdef_capnp.TaskList.from_bytes(self._socket.recv())
        for task in task_list.tasks:
            print(task.name)

if __name__ == "__main__":
    ts = TaskSubscriber()
    ts.get_task_list()
