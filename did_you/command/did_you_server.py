from did_you.server import TaskServer

def run_server():
    task_server = TaskServer()
    responder = threading.Thread(target=task_server.respond)
    responder.start()
    publisher = threading.Thread(target=task_server.publish)
    publisher.start()
