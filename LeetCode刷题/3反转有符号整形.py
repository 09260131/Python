# -*- coding:utf-8 -*-
# 创建日期: 2018-10-12

class Solution(object):
    def reverse(self, x):
        """
        :type x: int
        :rtype: int
        """
        if abs(x) < 10:
            return x
        res = 0
        y = abs(x)
        while y > 9:
            res = (res * 10) + (y % 10)
            y /= 10
        res = (res * 10) + (y % 10)
        return res if x > 0 else (0-res)


if __name__ == '__main__':
    x = Solution().reverse(-100)
    print(x)
