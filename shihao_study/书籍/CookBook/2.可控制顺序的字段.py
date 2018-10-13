# -*- coding:utf-8 -*-

from collections import OrderedDict

def testDict():
    td = OrderedDict()
    for i in range(20):
        td[i] = i*i

    print(td)

def reverseDict():
    prices = {
        'ACME': 45.23,
        'AAPL': 612.78,
        'IBM': 205.55,
        'HPQ': 37.20,
        'FB': 10.75
    }

    min_price = min(prices, key=lambda k: prices[k])  # Returns 'FB'
    max_price = max(prices, key=lambda k: prices[k])  # Returns 'AAPL'
    print(min_price, max_price)

def samplePonitDict():
    a = {
        'x': 1,
        'y': 2,
        'z': 3
    }
    b = {
        'w': 10,
        'x': 11,
        'y': 2
    }
    l = [1,2,3,4,5,6]
    print(l[1:])

def yeildTest():
    aaa = open('ttt.txt', 'r')
    print(aaa)
    if aaa:
        print('open')
    else:
        print('no open')
    aaa.close()
    print(aaa)
    if aaa:
        print('close')
    else:
        print('no close')

# python 实现 cat 命令
class cat:
    def __init__(self, files):
        self.files = files
        self.cur_file = None
    def __iter__(self):
        return self
    def next(self):
        while True:
            if self.cur_file:
                line = self.cur_file.readline()
                if line:
                    return line.rstrip()
                self.cur_file.close()
            if self.files:
                self.cur_file = open(self.files[0])
                self.files = self.files[1:]
            else:
                raise StopIteration()

# import sys
# def catTest(files):
#     for fn in files:
#         f = open(fn)
#         for line in f:
#             yield line.rstrip()
#
# if __name__ == '__main__':
#     if sys.argv[1:]:
#         for line in cat(sys.argv[1:]):
#            print(line)
#
# def tg():
#     print("hehe")
#     yield 1
#     yield 2
#     yield 3
#
# if __name__ == "__main__":
#     f = tg()
#     try:
#         print type(f)
#         while(True):
#             print(f.next())
#     except Exception, ex:
#         pass
#     print('finish all')

def dedupe(items):
    myset = set()
    for it in items:
        if it not in myset:
            myset.add(it)
    return myset

if __name__ == "__main__":
    print(list(dedupe([1,1,2,2,3,3,2,2,1,1])))



