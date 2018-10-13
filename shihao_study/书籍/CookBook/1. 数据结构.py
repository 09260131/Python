#!/usr/local/bin/python
# -*- coding:utf-8 -*-
import os
import sys

rows = [
{'fname': 'Brian', 'lname': 'Jones', 'uid': 1003},
{'fname': 'David', 'lname': 'Beazley', 'uid': 1002},
{'fname': 'John', 'lname': 'Cleese', 'uid': 1001},
{'fname': 'Big', 'lname': 'Jones', 'uid': 1004}
]

from operator import itemgetter
rows_by_fname = sorted(rows, key=itemgetter('fname'))
rows_by_uid = sorted(rows, key=itemgetter('uid'))
print(rows_by_fname)
print(rows_by_uid)



# project_path = os.path.abspath('../..')
# sys.path.append(project_path)
# os.environ['DJANGO_SETTINGS_MODULE'] = 'cmdb.settings'
# import django
# django.setup()
# from cmdb.configs import logger, logger_json
# import json
# from app.models import AppService, ServiceHost
# from host.models import Hosts
#
# if __name__ == '__main__':
    # service_name_id_dict = {}
    # for service in AppService.objects.filter(type='redis'):
    #     service_name_id_dict[service.name] = service.id
    # data = []
    # for name, id in service_name_id_dict.items():
    #     d = {'name': '', 'ips': []}
    #     d['name'] = name
    #     host_ids = [host.host_id for host in ServiceHost.objects.filter(service_id=id)]
    #     host_ips = [host.ip for host in Hosts.objects.filter(id__in=host_ids)]
    #     d['ips'] = list(set(host_ips))
    #     data.append(d)
    # print(data)

    # service_ids = [service.id for service in AppService.objects.filter(type='redis')]
    # host_ids = [host.host_id for host in ServiceHost.objects.filter(service_id__in=service_ids)]
    # host_ips = [host.ip for host in Hosts.objects.filter(id__in=host_ids)]
    # host_ips = list(set(host_ips))
    # print(host_ips)
import os, sys, redis, requests, json, base64, time

project_path = os.path.abspath('../..')
sys.path.append(project_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'cmdb.settings'
import django
django.setup()

from collections import deque
def test1():
    # 双端队列，可以从两端进行添加删除操作
    mylist = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    testDeque = deque(maxlen=10)
    for num in mylist:
        testDeque.append(num)
    print(testDeque)
    testDeque.appendleft(12)
    print(testDeque)
    testDeque.extendleft([13])
    print(testDeque)
    testDeque.popleft()
    print(testDeque)

def getTopFive():
    testDeque = deque(maxlen=5)
    with open('ttt.txt', 'r') as file:
        for f in file:
            if 'python' in f:
                testDeque.appendleft(f)
    print(testDeque)

import heapq
def getTopHeighData():
    data_list = [
        {'name': 'shihao', 'age': 22.5, 'sex': 'man'},
        {'name': 'yuanxuetao', 'age': 25.2, 'sex': 'man'},
        {'name': 'lining', 'age': 25.6, 'sex': 'man'},
        {'name': 'hehuanhuan', 'age': 25.6, 'sex': 'woman'},
        {'name': 'zhangning', 'age': 22.1, 'sex': 'man'},
        {'name': 'chengtongxin', 'age': 23.5, 'sex': 'man'},
    ]
    manlist = heapq.nlargest(3, data_list, key=lambda s:s['age'])
    print(manlist)
    manlist = heapq.nsmallest(3, data_list, key=lambda s: s['age'])
    print(manlist)
    man = heapq.heappop(manlist)
    print(man)

# 优先级队列
import itertools

pq = []                         # list of entries arranged in a heap
entry_finder = {}               # mapping of tasks to entries
REMOVED = '<removed-task>'      # placeholder for a removed task
counter = itertools.count()     # unique sequence count
# print(pq, entry_finder, REMOVED, counter, next(counter), next(counter))

def add_task(task, priority=0):
    'Add a new task or update the priority of an existing task'
    if task in entry_finder:
        remove_task(task)
    count = next(counter)
    entry = [priority, count, task]
    entry_finder[task] = entry
    heapq.heappush(pq, entry)

def remove_task(task):
    'Mark an existing task as REMOVED.  Raise KeyError if not found.'
    entry = entry_finder.pop(task)
    entry[-1] = REMOVED

def pop_task():
    'Remove and return the lowest priority task. Raise KeyError if empty.'
    while pq:
        priority, count, task = heapq.heappop(pq)
        if task is not REMOVED:
            del entry_finder[task]
            return task
    raise KeyError('pop from an empty priority queue')

def work1():
    print('work, work!')

def work2():
    print('work2, work2!')

def work3():
    print('work3, work3!')

def work4():
    print('work4, work4!')

if __name__ == '__main__':
    # getTopFive()
    # getTopHeighData()
    # 测试优先级队列
    add_task(work1, 1)
    print(pq, entry_finder)
    add_task(work2, 2)
    print(pq, entry_finder)
    add_task(work3, 3)
    print(pq, entry_finder)
    add_task(work4, 4)
    print(pq, entry_finder)
    remove_task(work2)
    print(pq, entry_finder)

    try:
        task = pop_task()
        task()

        task = pop_task()
        task()

        task = pop_task()
        task()

        task = pop_task()
        task()

    except Exception, ex:
        print(str(ex))































