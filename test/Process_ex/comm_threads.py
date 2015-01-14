__author__ = 'Administrator'

from multiprocessing import Process, Queue
import os, time, random

#write data into sub-process
def write(q):
    for value in ['a', 'b', 'c']:
        print 'Put %s to queue...' % value
        q.put(value)
        time.sleep(random.random())

#read data from sub-process
def read(q):
    while True:
        value = q.get(True)
        print 'Get %s from queue.' % value

if __name__ == '__main__':
    #create Queue
    q = Queue()
    pw = Process(target = write,args=(q,))
    pr = Process(target = read, args=(q,))
    pw.start()
    pr.start()
    pw.join()
    pr.terminate()

