# -*- coding: utf-8 -*-
import json
import os
import sys
import time

project_path = os.path.abspath('../..')
sys.path.append(project_path)

from syncTask.redis.mq import Q

class Task():

    queue_key = "cmdb_task"

    def excute(self, **kwargs):
        return True, 'succ!'

    def addTask(self, **kwargs):
        try:
            q = Q(self.queue_key)
            kwargs['task'] = str(self.__class__)
            print(kwargs)
            q.push(json.dumps(kwargs))
        except Exception, ex:
            print('addTask %s' % str(ex))

    def run(self, **kwargs):
        try:
            res, data = self.excute(**kwargs)
            state = 'failure'
            if res:
               state = 'success'
            print('runTask %s' % state)
        except Exception, ex:
            print('runTask %s' % str(ex))

class testTask(Task):

    def excute(self, **kwargs):
        try:
            time.sleep(10)
            print(kwargs)
            return True, 'down'
        except Exception, ex:
            return False, str(ex)

if __name__ == '__main__':
    param_dict = {
        'params': '{"name": "shihao", "wife": "hhh"}'
    }
    testTask().addTask(**param_dict)