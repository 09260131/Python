import threading
import time

def showThreadInfo(c):

    # print("ct = {}".format(threading.current_thread()))
    # print("mt = {}".format(threading.main_thread()))
    # print("ac = {}".format(threading.active_count()))

    count = 0
    while True:
        if count > c:
            raise RuntimeError
        # print "I am working"
        # print threading.current_thread().name
        time.sleep(1)
        count += 1

# def worker1(a):
#     print a
#     time.sleep(1)
#     print '1 over'
#
# def worker2(a):
#     print a
#     time.sleep(1)
#     print '2 over'

if __name__ == "__main__":

    t = threading.Thread(target=showThreadInfo, name='worker', args=(5,))
    t.start()

    if t.is_alive():
        print t.ident, t.name, t.ident, t.name