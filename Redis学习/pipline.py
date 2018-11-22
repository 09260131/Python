# -*- coding:utf-8 -*-

from redisconnection import Conn

class Pipline(Conn):

    def getpipline(self):
        return self.__conn.pipeline()

def test():
    import redis
    c = redis.Redis(host='localhost',port=6379,db=0).pipeline()
    pipline = c.pipeline()
    pipline.set('hello1', 'redis1')
    pipline.set('hello2', 'redis2')
    pipline.set('hello3', 'redis3')
    pipline.set('hello4', 'redis4')
    pipline.set('hello5', 'redis5')
    pipline.execute()

    print c.get('hello1')



if __name__ == '__main__':

    test()