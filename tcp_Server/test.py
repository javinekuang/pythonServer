__author__ = 'Administrator'
# coding=utf-8

import threading
from Queue import Queue


class ClientThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.flag = True

    def run(self):
        counter = 0
        current_counter = 0
        global queue
        global q_counter
        while self.flag:
            counter += 1
            if counter > 10:
                self.flag = False
            print "input data " + threading.current_thread().getName()
            data = raw_input()

            data1 = data.split(",")
            print data1

            if "javine" in data:
                if usernameDict.has_key("javine"):
                    queue[usernameDict["javine"]].put(data)
                else:
                    usernameDict["javine"] = q_counter
                    queue.append(Queue())
                    q_counter += 1
                    queue[usernameDict["javine"]].put(data)
            elif data == "get":
                if queue[usernameDict["javine"]].empty() is False:
                    print queue[usernameDict["javine"]].get() + "----" + threading.current_thread().getName()
                else:
                    print "the %s queue is empty"%"javine"
            else:
                if len(queue) > usernameDict["javine"]:
                    queue[usernameDict["javine"]].put(data)
            #decode(data)


if __name__ == "__main__":
    usernameDict = {}
    queue = []
    q_counter = 0
    #while 1:
    print "please input [new]:"
    if raw_input() == "new":
        ClientThread().start()