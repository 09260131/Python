# -*- coding: utf-8 -*-

class Node(object):
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkList(object):
    def __init__(self, data_list):
        self.head = Node('head')
        tail = self.head
        for data in data_list:
            tail.next = Node(data)
            tail = tail.next

    def __str__(self):
        data = self.head
        s = ''
        while data:
            s += str(data.data) + str('->')
            data = data.next
        return s

    def len(self):
        data = self.head
        len = 0
        while data.next:
            len += 1
            data = data.next
        return len

    def empty(self):
        return not self.len()

    def append(self, num):
        data = self.head
        while data.next:
            data = data.next
        data.next = Node(num)

    def getItem(self, index):
        if (index >= self.len()) or (index < 0):
            print(u'index out of range')
            return False, 'error'
        data = self.head.next
        now_index = 0
        while data:
            if now_index == index:
                print('data = %s' % str(data.data))
                return True, data.data
            else:
                now_index += 1
                data = data.next

    def find(self, num):
        data = self.head.next
        index = 0
        while data:
            if data.data == num:
                return True, index
            else:
                data = data.next
                index += 1
        return False, 'not found!'

    def insert(self, index, num):
        if (index < 0) or (index >= self.len()):
            return False, 'out of range!'
        data = self.head
        now_index = 0
        while (now_index != index):
            now_index += 1
            data = data.next
        next_node = data.next
        node = Node(num)
        data.next = node
        node.next = next_node

    def delete(self, index):
        if (index < 0) or (index >= self.len()):
            return False, 'out of range!'
        data = self.head
        now_index = 0
        while now_index != index:
            now_index += 1
            data = data.next
        next_data = data.next
        data.next = next_data.next

    def update(self, index, num):
        if (index < 0) or (index >= self.len()):
            return False, 'out of range!'
        data = self.head.next
        now_index = 0
        while now_index != index:
            now_index += 1
            data = data.next
        data.data = num

    def clear(self):
        self.head = None



if __name__ == '__main__':
    ll = LinkList([1,2,3,4,5,6,7,8,9,0])
    print(ll.insert(3, 100))
    print(ll.delete(-1))
    print(ll.update(10, 100))
    print(ll)
    ll.clear()
    print(ll)