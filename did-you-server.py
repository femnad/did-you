#!/usr/bin/env python3
import msgpack
import redis
import threading
import zmq

from did_you_config import DidYouConfig


class TaskServer(object):

    task_list_key = 'tasklist'

    def __init__(self):
        configurator = DidYouConfig()
        self.redis_client = redis.Redis(
            host=configurator.redis_host, port=configurator.redist_port)
        self.respond_port = configurator.request_port
        self.publish_port = configurator.subscription_port

    def respond(self):
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://*:{}".format(self.respond_port))
        while True:
            message = socket.recv()
            task_message = msgpack.unpackb(message)
            task_name = task_message[b'name']
            command = task_message[b'command']
            response = None
            if command == b'do':
                response = self.redis_client.sadd(self.task_list_key, task_name)
            elif command == b'done':
                response = self.redis_client.srem(self.task_list_key, task_name)
            else:
                response = b'Nack'
            if response == 1:
                socket.send(b'Ack')
            else:
                socket.send(b'Nack')

    def publish(self):
        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        socket.bind("tcp://*:{}".format(self.publish_port))
        while True:
            tasks = self.redis_client.smembers(self.task_list_key)
            task_list = list(tasks)
            socket.send(msgpack.packb(task_list))

if __name__ == "__main__":
    task_server = TaskServer()
    responder = threading.Thread(target=task_server.respond)
    responder.start()
    publisher = threading.Thread(target=task_server.publish)
    publisher.start()
