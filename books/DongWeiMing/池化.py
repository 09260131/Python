# -*- coding: utf-8 -*-

class A:
    def __init__(self, a):
        self.a = a

    @property
    def key(self):
        return self.a

    def __eq__(self, other):
        return self.key == other.key



if __name__ == '__main__':

    d = {}
    a1 = A(1)
    a2 = A(1)
    print a1 == a2

    # d[A(1)] = 10
    # d[A(1)] = 20
    # print d
    # print d[a1], d[a2]

    # s1 = 'hello'
    # s2 = 'hello'
    # print s1 is s2
    #
    # s3 = 'hello world'
    # s4 = 'hello world'
    # print s3 is s4

    # d1 = dict.fromkeys(['a', 'b', 'c'], '111')
    # print d1
    #
    # d2 = dict.fromkeys(['d', 'e', 'f'], '222')
    # print d2
    #
    # d3 = dict(d1, **d2)
    # print d3
    # d3.setdefault('h', '333')
    # print d3
    #
    # print d3.setdefault('h', '444')

    # 字符串中每个字符出现的次数
    # s = 'asdfawefadafeaf'
#     # d = {}
#     # for c in s:
#     #     d[c] = d.setdefault(c, 0) + 1
#     # print d
#     #
#     # import collections
#     # d = collections.defaultdict(int)
#     #
#     # for c in s:
#     #     d[c] += 1
#     # print d
#     # print d['a'], d['e']
