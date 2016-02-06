#!/usr/bin/env python3
from sh import notify_send
from time import sleep

from did_you_client import TaskSubscriber
from did_you_config import DidYouConfig

if __name__ == "__main__":
    configurator = DidYouConfig()
    sleep_period = int(configurator.sleep_period)

    task_subscriber = TaskSubscriber()

    while True:
        task_list = task_subscriber.get_task_list()
        if len(task_list) > 0:
            task_notification = ["{}: {}".format(index, str(task, 'UTF-8'))
                                 for index, task in enumerate(task_list, 1)]
            notify_send("TODO:", "\n".join(task_notification))
        sleep(sleep_period)
