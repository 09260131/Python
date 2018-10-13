# !/usr/bin/python
# -*- coding: utf-8 -*-
# ScriptName: 合并两个无序数组
# CreateTime: 2018-06-01
# UpdateTime: 2018-06-01
import numpy

def mergeTwoList(l1, l2):
    len1 = len(l1)
    len2 = len(l2)
    l3 = []
    index = 0
    while((index < len1) or (index < len2)):
        if index < len1:
            l3.append(l1[index])
        if index < len2:
            l3.append(l2[index])
        index = index + 1
    return l3



if __name__ == '__main__':
    l1 = numpy.random.randint(100, size=10)
    l2 = numpy.random.randint(100, size=6)
    print(l1)
    print(l2)
    l3 = mergeTwoList(l1, l2)
    print(l3)