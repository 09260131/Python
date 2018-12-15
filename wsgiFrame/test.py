# -*- coding:utf-8 -*-

d = {
    'a': 100,
    'c': 300,
    'd': 400
}

class DictObj:

    def __init__(self, d):
        # self._dict = d
        print d

    # 递归保护
    def __getattr__(self, item):
        print 'hello'
        return self._dict[item]
        # try:
        #     return self._dict[item]
        # except KeyError:
        #     raise AttributeError('Attribute {} Not Found.'.format(item))

    # def __setattr__(self, key, value):
    #     print key, value


if __name__ == '__main__':

    print 'hello'
    # d = DictObj(d)
    # print d.e