#!/usr/bin/env python

import sqlite3

con = sqlite3.connect("lesson.db")	#若不存在则新建数据库
cur = con.cursor()			            #获取数据库游标
sql = "insert into lesson_info values ('%s', '%s','%s','%s','%s','%s')" % (name, link, des, number, time, degree)
cur.execute(sql)			              #执行SQL
con.commit()				                #提交事务

