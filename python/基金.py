# -*- coding:utf-8 -*-  

import requests
import threading
import re
import os
import time
from bs4 import  BeautifulSoup
import sqlite3

def createdb(name):
    try:
        conn = sqlite3.connect(name)
        conn.execute(
            '''CREATE TABLE record
           (
                Time     CHAR(50),
                Value     CHAR(50)
           );
           ''')
        print "DB_name:\t%s" %(name)
        conn.close()
    except:
        print "Create DB Error..."

record={}
db_name=str(time.strftime('%Y-%m-%d_%H',time.localtime(time.time()))+'.db')
conn = sqlite3.connect(db_name)

#获取网页HTML结构
def html_info(url):
    element=requests.get(str(url)).text
    html=BeautifulSoup(element,'html.parser')
    html_string=html.select("#gz_gszzl")  #ID!
    x=re.compile(r'(?<=>).*%')            #正则
    v=x.findall(str(html_string))[0]      #匹配
    t=time.strftime('%Y-%m-%d:%H:%M',time.localtime(time.time()))
    sql="INSERT INTO record (Time,Value) VALUES ('%s','%s')" %(t,v)
    conn.execute(sql)
    conn.commit()
    print "%s \t %s" %(v,t)

if __name__ == '__main__':
    createdb(name=db_name)
    while True:
        html_info(url='http://fund.eastmoney.com/003625.html?spm=search')
        time.sleep(1)
        if str(time.strftime('%H:%S',time.localtime(time.time()))) == "15:01":
            conn.close()
            break
