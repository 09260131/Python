# -*- coding: utf -8 -*-
import os
import sys

project_path = os.path.abspath('../..')
sys.path.append(project_path)

import importlib
import json
import new
from multiprocessing import Process
from syncTask.redis.mq import Q


def run_task_job(queue_key):
    q = Q(queue_key)
    while True:
        msg = q.pop()
        try:
            print msg
            task_data = json.loads(msg[1])
            task = task_data['task']
            task = 'syncTask.task.task.testTask'
            task_list = task.split(".")
            module = importlib.import_module(".".join(task_list[:-1]))
            reload(module)
            TaskClass = getattr(module, task_list[-1])
            obj = new.instance(TaskClass)
            obj.run(**json.loads(task_data['params']))
        except Exception, ex:
            print str(ex)

if __name__ == "__main__":

    proc_record = []
    for i in range(10):
        p = Process(target=run_task_job, args=('cmdb_task', ))
        p.start()
        proc_record.append(p)
    for proc in proc_record:
        p.join()

