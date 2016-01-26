#!/usr/bin/env python3
import threading
import zmq

_tasks = set()


def serve_rep():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")
    while True:
        message = str(socket.recv(), 'utf-8')
        command, task_name = message.split(':')
        if command == 'do':
            _tasks.add(task_name)
        elif command == 'done':
            _tasks.remove(task_name)
        socket.send(b'ack')


def publish():
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5556")
    while True:
        task_list = '\n'.join([t for t in _tasks])
        socket.send(bytes(task_list, 'utf-8'))


if __name__ == "__main__":
    rep = threading.Thread(target=serve_rep)
    rep.start()
    pub = threading.Thread(target=publish)
    pub.start()
