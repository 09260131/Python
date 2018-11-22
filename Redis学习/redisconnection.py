# -*- coding:utf-8 -*-

import redis

class Conn(object):

    def __init__(self, Host='localhost', Port=6379):
        self.__conn = redis.Redis(host=Host, port=Port)