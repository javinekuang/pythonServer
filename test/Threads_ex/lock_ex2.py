__author__ = 'Administrator'

import time
import threading

balance = 0
lock = threading.Lock()

def change_it(n):
    global balance
    balance = balance + n
    balance = balance - n

def run_thread(n):
    print 'run thread %s...' % n
    for i in range(100000):
        lock.acquire()
        try:
            change_it(n)
        finally:
            lock.release()


t1 = threading.Thread(target=run_thread, args=(5,))
t2 = threading.Thread(target=run_thread, args=(8,))
start = time.time()
t1.start()
t2.start()
t1.join()
t2.join()
end = time.time()
print balance
print 'this code takes %0.2f s' % (end - start)

