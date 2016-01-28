#!/usr/bin/env python3
import capnp
import redis
import taskdef_capnp
import threading
import zmq

from did_you_config import DidYouConfig


class TaskServer(object):

    task_list_key = 'tasklist'

    def __init__(self):
        self.redis_client = redis.Redis()
        configurator = DidYouConfig()
        self.respond_port = configurator.request_port
        self.publish_port = configurator.subscription_port

    def respond(self):
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://*:{}".format(self.respond_port))
        while True:
            message = socket.recv()
            task_message = taskdef_capnp.TaskMessage.from_bytes(message)
            task_name = task_message.task.name
            command = task_message.command
            if command == 'do':
                self.redis_client.sadd(self.task_list_key, task_name)
            elif command == 'done':
                self.redis_client.srem(self.task_list_key, task_name)
            socket.send(b'ack')

    def publish(self):
        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        socket.bind("tcp://*:{}".format(self.publish_port))
        while True:
            tasks = self.redis_client.smembers(self.task_list_key)
            number_of_tasks = len(tasks)
            tasklist_message = taskdef_capnp.TaskList.new_message()
            tasklist_message.init('tasks', number_of_tasks)
            for index, task in enumerate(tasks):
                tasklist_message.tasks[index] = {'name': task}
            socket.send(tasklist_message.to_bytes())

if __name__ == "__main__":
    task_server = TaskServer()
    responder = threading.Thread(target=task_server.respond)
    responder.start()
    publisher = threading.Thread(target=task_server.publish)
    publisher.start()
