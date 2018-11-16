# -*- coding: utf-8 -*-
import redis

####################################################################

REDIS_HOST = '127.0.0.1'

####################################################################

class RedisHealthCheck():
    state = False
    def __init__(self, host=REDIS_HOST, port=6379):
        try:
            self.__conn = redis.Redis(host=host, port=port)
            self.state = True
        except Exception as ex:
            print str(ex)
            self.state = False