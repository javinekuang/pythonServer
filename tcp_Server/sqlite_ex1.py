__author__ = 'Administrator'

import sqlite3


conn = sqlite3.connect('test.db')
cursor = conn.cursor()
#cursor.execute("create table user (id integer primary key,username varchar(10) UNIQUE,password text NULL)")
cursor.execute("create table if not exists devMac (id integer primary key,mac varchar(12) UNIQUE)")

#for t in [(5,"javinek","19870825"),(6,"funnyj","19960102")]:
#    cursor.execute("insert into user values (?,?,?)",t)

#cursor.execute("insert into devMac values (?,?)",(3,"ADCB233B5CAD"))

cursor.execute("select * from user where username like 'kuang'")
values = cursor.fetchall()
print len(values)

cursor.execute("select * from devMac where mac like 'A%'")
values = cursor.fetchall()
print values
cursor.close()

conn.commit()
conn.close()
