# -*- coding:utf-8 -*-
# 创建日期: 2018-10-15

# Definition for singly-linked list.
class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution(object):
    def addTwoNumbers(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """
        num = 1
        sum = 0
        while l1 or l2:
            if l1:
                sum += num * l1.val
                l1 = l1.next
            if l2:
                sum += num * l2.val
                l2 = l2.next
            num *= 10

        num_list = []
        if sum == 0:
            num_list.append(sum)
        while sum:
            num_list.append(sum%10)
            sum /= 10
        head = ListNode(-1)
        pointer = head
        for num in num_list:
            pointer.next = ListNode(num)
            pointer = pointer.next
        return head.next




if __name__ == '__main__':
    a = ListNode(1)
    b = ListNode(2)
    c = ListNode(3)
    d = ListNode(4)
    e = ListNode(5)
    f = ListNode(6)
    a.next = b
    b.next = c
    c.next = d
    d.next = e
    e.next = f

    aa = ListNode(1)
    bb = ListNode(2)
    cc = ListNode(0)
    aa.next = bb
    bb.next = cc

    num = Solution().addTwoNumbers(a, aa)
    while num:
        print(num.val)
        num = num.next