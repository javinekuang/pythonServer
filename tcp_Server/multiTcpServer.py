__author__ = 'Administrator'
# coding=utf-8

import socket
import sys
import threading
import Queue
import random
import os
import time
import login

###
HOST = "0.0.0.0"
PORT = 25565
SOCK_ADDR = (HOST, PORT)
###


class SocketClientObject(object):
    def __init__(self, sockets, address):
        self.socket = sockets
        self.address = address
###


class MyQueue():
    def __init__(self,username):
        self.map = {username: ""}
        self.username = username

    def put(self, string):
        item = string.split(',')
        if self.username not in self.map.keys():
            self.map[self.username] = ""
        if item[0] == self.username:
            self.map[item[0]] = self.map[item[0]] + ',' + item[1]
        else:
            self.map[item[0]] = item[1]

    def pop(self,key):
        #如果key存在，返回key的value值，并删除key
        if key in self.map.keys():
            return self.map.pop(key)
        else:
            return 0


class MsgList():
    def __init__(self):
        self.list = []
        self.dict = {}
        self.index = 0

    def isContains(self,username):
        if username in self.dict.keys():
            return True
        else:
            return False

    def add(self, username, myqueue):
        self.dict[username] = self.index
        self.index += 1
        self.list.append(myqueue)

    def get(self,username):
        print "the length of my list is %d" % len(self.list)
        if username in self.dict.keys() and len(self.list) > 0:
            print "%s Queue is returned." % username
            return self.list[self.dict[username]]
        return None


#控制线程：登录成功后，与app和终端通信线程
class DealThread(threading.Thread):
    def __init__(self, client_object, username):
        threading.Thread.__init__(self)
        self.client_object = client_object
        self.flag = True
        self.username = username
        self.client_object.socket.settimeout(20)   #10s未接收到数据，断开连接

    def run(self):
        print "Deal Thread is running..."
        myqueue = mlist.get(self.username)
        while self.flag:
            try:
                data = self.client_object.socket.recv(1024)
                back = decode_cmd(data.strip())
                username = back[0]
                mac = back[1]
                if myqueue is None:
                    myqueue = mlist.get(self.username)
                    print "queue is None"
                else:
                    myqueue.put(data)
                    print "save cmd!"
                    cmd = myqueue.pop("javine")
                #cmd = mlist.get(self.username).pop(username)
                if cmd is not 0:
                    self.client_object.socket.sendall(cmd)
                print data
            except:
                print "#! EXC: ", sys.exc_info()
                self.client_object.socket.sendall("TimeOut Error!")
                self.flag = False
        #无连接，关闭socket
        self.client_object.socket.close()


class DevThread(threading.Thread):
    def __init__(self, client_object, username):
        threading.Thread.__init__(self)
        self.client_object = client_object
        self.flag = True
        self.username = username
        self.client_object.socket.settimeout(20)

    def run(self):
        print "DEV Thread is running..."
        myqueue = mlist.get(self.username)
        while self.flag:
            try:
                data = self.client_object.socket.recv(1024)
                back = decode_cmd(data.strip())
                mac = back[0]
                nice = back[1]
                if myqueue is None:
                    myqueue = mlist.get(self.username)
                    print "queue is None"
                else:
                    myqueue.put("javinek,kuang")
                    print "save cmd!"

                print data
            except:
                print "#! EXC: ", sys.exc_info()
                self.client_object.socket.sendall("TimeOut Error!")
                self.flag = False
        #无连接，关闭socket
        self.client_object.socket.close()

def decode_cmd(c):
    cmd = c.split(",")
    if len(cmd) > 1:
        return cmd
    return None


#登录线程：注册，登录，启动控制线程
class LoginThread(threading.Thread):
    def __init__(self, client_object):
        threading.Thread.__init__(self)
        self.client_object = client_object
        #判断此线程是否关闭socket
        self.flag = True
        self.username = ""

    def run(self):
        data = self.client_object.socket.recv(1024)
        data = data.strip()
        re_value = self.decode(data)
        if re_value == 'R':
            back_data = "register success."
        elif re_value == 'RF':
            back_data = "username is used!"
        elif re_value == 'F':
            back_data = "username or password wrong"
        elif re_value == 'E':
            back_data = "wrong data..."
        elif re_value == 'MF':
            back_data = "No active MAC address."
        else:
            back_data = 'connect success.'
            self.flag = False
            #加锁
            if mlist.isContains(self.username) is False:
                global mqueue
                mqueue = MyQueue(self.username)
                mlist.add(self.username, mqueue)
            if re_value == 'DEV':
                det = DevThread(self.client_object, self.username)
                det.start()
            elif re_value == 'DEAL':
                dt = DealThread(self.client_object, self.username)
                dt.start()

        print ">> Received data: ", data, " from: ", self.client_object.address
        self.client_object.socket.sendall(back_data)
        #Connect Success ,client socket do not close
        if self.flag:
            self.client_object.socket.close()

    def decode(self,d):
        rdata = d.split(",")
        print rdata
        if len(rdata) > 2:
            if rdata[0] == "register":
                if len(login.Login.get_login(rdata[1])) == 0:
                    login.Login.save_login(rdata[1],rdata[2])
                    return 'R'
                else:
                    return 'RF'
            elif rdata[0] == "login":
                info = login.Login.get_login(rdata[1])
                if len(info) > 0:
                    if info[0][2] == rdata[2]:
                        #返回登录的username
                        self.username = info[0][1]
                        return 'DEAL'
                return 'F'
            elif rdata[0] == "mac":
                info = login.Login.get_mac(rdata[1])
                if len(info) > 0:
                    #与mac对应的username
                    self.username = info[0][1]
                    return 'DEV'
                return 'MF'
        else:
            return 'E'


def main():
        print "TCP server is running..."
        login.Login()
        global mlist
        mlist = MsgList()
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(SOCK_ADDR)
            sock.listen(100)
            while 1:
                # accept connections from outside
                (clientsocket, address) = sock.accept()
                print "# Accept client: ", address
                # now do something with the clientsocket
                # in this case, we'll pretend this is a threaded server
                lt = LoginThread( SocketClientObject(clientsocket, address))
                lt.start()
        except:
            print "#! EXC: ", sys.exc_info()
            sock.close()
            print "THE END! Goodbye!"
###
if __name__ == "__main__":
    main()
