import random




# def max_min(x, y, *args):
#     max_num = max(x, y)
#     min_num = min(x, y)
#     for num in args:
#         if num > max_num:
#             max_num = num
#         if num < min_num:
#             min_num = num
#     return max_num, min_num

# print(*max_min(*[random.randint(1, 100) for _ in range(10)]))

# def max_min(*args):
#     max_num = 0
#     min_num = 0
#     if args[0] > args[1]:
#         max_num = args[0]
#         min_num = args[1]
#     else:
#         max_num = args[1]
#         min_num = args[0]
#     if len(args) > 2:
#         for num in args[2:-1]:
#             if num > max_num:
#                 max_num = num
#             if num < min_num:
#                 min_num = num
#     print(max_num, min_num)

# max_min(*[1,2,3,4,5,6,7,8,9,0])




def triangle(num):
    x = num + 1
    y = num + 1
    for i in range(1, x):
        for j in range(1, y):
            print str(j),
        print('\n')
        y -= 1

def triangle1(num):
    x = num + 1
    y = num + 1
    for i in range(1, x+1):
        for j in range(y, 0, -1):
            if i >= j:
                print str(j),
            else:
                print len(str(j)) * ' ',
        print('\n')

if __name__ == '__main__':
    triangle1(10)







