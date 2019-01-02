# -*- coding:utf-8 -*-

d = {
    'a': 100,
    'c': 300,
    'd': 400
}

class DictObj:

    def __init__(self, d):
        self._dict = d

    # 递归保护
    def __getattr__(self, item):
        try:
            return self._dict[item]
        except KeyError:
            raise AttributeError('Attribute {} Not Found.'.format(item))

class Context(dict):

    def __getattr__(self, item):
        try:
            return self[item]
        except Exception, ex:
            raise AttributeError('Attribute {} Not Found.'.format(item))

    def __setattr__(self, key, value):
        self[key] = value

class NestedContext(Context):

    def __init__(self, globalcontext=None):
        super(NestedContext, self).__init__()
        self.globalcontext = globalcontext

    def relate(self, globalcontext=None):
        self.globalcontext = globalcontext

    def __getattr__(self, item):
        if item in self.keys():
            return self[item]
        return self.globalcontext[item]




if __name__ == '__main__':

    c = Context()
    c['a'] = 10
    c['b'] = 20
    c['c'] = 30
    print c
    print c.ad
    print c.d

    # nc = NestedContext()
    # nc.relate(c)
    # nc['c'] = 300
    # nc['d'] = 400
    # print nc
    # print nc.a
    # print nc.c
    # print nc.d
    # print nc.e

    # a = Context()
    # a['1'] = 1
    # a['2'] = 2
    # a['3'] = 3
    # print a
    # print a['1']


    # d = DictObj(d)
    # print d.a