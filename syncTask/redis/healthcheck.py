# -*- coding: utf-8 -*-
import redis

####################################################################

REDIS_HOSTS = ['127.0.0.1', '192.168.0.103', '35.221.198.70', '45.76.9.111']

####################################################################

class RedisHealthCheck():
    state = False
    def __init__(self, host, port=6379):
        try:
            self.__conn = redis.Redis(host=host, port=port)
            self.state = True
        except Exception as ex:
            print str(ex)
            self.state = False

if __name__ == '__main__':
    for host in REDIS_HOSTS:
        print host, RedisHealthCheck(host=host).state