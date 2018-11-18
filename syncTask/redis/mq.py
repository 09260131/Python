# -*- coding: utf-8 -*-
import sys
import redis

####################################################################

REDIS_HOST = '192.168.0.104'

####################################################################

class Q():
    def __init__(self, key, host=REDIS_HOST, port=6379):
        self.__conn = redis.Redis(host=host, port=port)
        self.key = key

    def push(self, msg, key=''):
        if not key:
            print(key)
            key = self.key
        self.__conn.lpush(key, msg)

    def pop(self, key=''):
        if not key:
            key = self.key
        return self.__conn.blpop(key)