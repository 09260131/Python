# !/usr/bin/python
# -*- coding: utf-8 -*-
# ScriptName:
# CreateTime: 2018-06-04
# UpdateTime: 2018-06-04
import numpy

# 数组中奇数个数的数字(只有个一个数字是奇数个其余的都是偶数个)
def findOddFigure(test):
    result = 0
    for figure in test:
        result = result ^ figure
    print(result)

# 数组中只有一个数出现一次其余都出现三次, 找出这个数
def findOddFigureII(test):
    one = 0
    two = 0
    for i in range(len(test)):
        two |= test[i] & one         # two为1时，不管A[i]为什么，two都为1
        print(bin(two))
        one = test[i] ^ one          # 异或操作，都是1就进位
        print(bin(one))
        three = ~(one & two)         # 以下三步的意思是：如果one和two都为1时，就清0，反之则保持原来状态。
        print(bin(three))
        one &= three
        print(bin(one))
        two &= three
        print(bin(two))

        print(one)
    print(one)


if __name__ == '__main__':
    # test = [1,2,3,1,2,3,4,5,6,4,5,6,7,8,9,7,8,9,9]
    # findOddFigure(test)

    test = [1, 1, 1, 2]
    findOddFigureII(test)
