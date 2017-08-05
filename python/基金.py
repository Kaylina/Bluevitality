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
        print "DB name: \t %s" %(str(os.getcwd())+'\\'+name)
        conn = sqlite3.connect(name)
        conn.execute('''CREATE TABLE record(Time CHAR(50),Value CHAR(50));''')
        conn.close()
    except:
        print "Create DB Error..."

record={}
db_name=str(time.strftime('%Y-%m-%d_%H',time.localtime(time.time()))+'.db')
conn = sqlite3.connect(db_name)

#获取网页HTML结构
def html_info(url):
    html_string=BeautifulSoup(requests.get(str(url)).text,'html.parser').select("#gz_gszzl")
    v=re.compile(r'(?<=>).*%').findall(str(html_string))[0]            #正则
    t=time.strftime('%Y-%m-%d:%H:%M',time.localtime(time.time()))
    print "%s \t %s" %(v,t)
    sql="INSERT INTO record (Time,Value) VALUES ('%s','%s')" %(t,v)
    conn.execute(sql)
    conn.commit()

if __name__ == '__main__':
    createdb(name=db_name)
    while True:
        html_info(url='http://fund.eastmoney.com/003625.html?spm=search')
        time.sleep(60)
        if str(time.strftime('%H:%S',time.localtime(time.time()))) == "15:01":
            conn.close()
            break
