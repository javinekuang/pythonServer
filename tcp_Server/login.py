__author__ = 'Administrator'
#coding=utf-8

import sqlite3

#保存注册信息
#提取注册信息
#查询注册信息与MAC值


class Login():

    def __init__(self):
        cn = sqlite3.connect("userInfo.db")
        cur = cn.cursor()
        cur.execute("create table if not exists user(id integer primary key,username varchar unique,password varchar)")
        cur.execute("create table if not exists mac(id integer primary key,username varchar,mac varchar unique)")
        cur.close()
        cn.commit()
        cn.close()

    @staticmethod
    def save_login(username,password):
        cn = sqlite3.connect("userInfo.db")
        cur = cn.cursor()
        cur.execute("insert into user values (?,?,?)",(None,username,password))
        cur.close()
        cn.commit()
        cn.close()

    @staticmethod
    def save_mac(username,mac):
        cn = sqlite3.connect("userInfo.db")
        cur = cn.cursor()
        cur.execute("insert into mac values (?,?,?)",(None,username,mac))
        cur.close()
        cn.commit()
        cn.close()

    @staticmethod
    def get_login(username):
        cn = sqlite3.connect("userInfo.db")
        cur = cn.cursor()
        cur.execute("select * from user where username like ?",(username,))
        info = cur.fetchall()
        cur.close()
        cn.commit()
        cn.close()
        return info

    @staticmethod
    def get_mac(username):
        cn = sqlite3.connect("userInfo.db")
        cur = cn.cursor()
        cur.execute("select * from mac where username like ?",(username,))
        info = cur.fetchall()
        cur.close()
        cn.commit()
        cn.close()
        return info

    @staticmethod
    def get_by_mac(mac):
        cn = sqlite3.connect("userInfo.db")
        cur = cn.cursor()
        cur.execute("select * from mac where mac like ?",(mac,))
        info = cur.fetchall()
        cur.close()
        cn.commit()
        cn.close()
        return info