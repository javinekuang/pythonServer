__author__ = 'Administrator'
# coding=utf-8

import threading
import login
import time
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
            data = data.strip()
            data1 = data.split(",")
            print data1
            if data1[0] == "get":
                username = data1[1]
            else:
                username = data1[0]
                password = data1[1]

            if len(username) > 0:
                if usernameDict.has_key(username):
                    queue[usernameDict[username]].put(data)
                else:
                    usernameDict[username] = q_counter
                    queue.append(Queue())
                    q_counter += 1
                    queue[usernameDict[username]].put(data)
            elif data1 == "get":
                if queue[usernameDict["javine"]].empty() is False:
                    print queue[usernameDict["javine"]].get() + "----" + threading.current_thread().getName()
                else:
                    print "the %s queue is empty"%"javine"
            #decode(data)


class ActionThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            print "input action:"+threading.current_thread().getName()
            data = "good" #raw_input()
            if data == "register":
                ClientThread().start()
            time.sleep(1)


if __name__ == "__main__":
    usernameDict = {}
    queue = []
    q_counter = 0
    login.Login()
    #login.Login.save_mac("JAVK","198708s25")
    #login.Login.save_mac("JAVK","19870e825")
    #login.Login.save_mac("JAVK","19870d825")
    info = login.Login.get_by_mac("19870d825")
    print len(info)
    print info
    while 1:
        print "please input [new]:"
        if raw_input() == "new":
            ActionThread().start()