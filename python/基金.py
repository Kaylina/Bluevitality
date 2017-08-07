
# -*- coding:utf-8 -*-  

import requests
import multiprocessing
import re
import os
import time
from bs4 import  BeautifulSoup
import sqlite3

db_name=str(time.strftime('sqlite.'+'%Y-%m',time.localtime(time.time()))+'.db')
conn = sqlite3.connect(db_name)

def createdb(name):
    try:
        conn = sqlite3.connect(name)
        conn.execute('''CREATE TABLE record(Name CHAR(10),Value CHAR(50),nTime CHAR(50));''')
        conn.close()
    except:
        print "already exists %s file..." %(name)
    else:
        print "DB name: \t %s" %(str(os.getcwd())+'\\'+name)


def html_info(url,name,times):
        if str(time.strftime('%H:%S',time.localtime(time.time()))) == "15:02":
            conn.close()
            os.exit()
        time.sleep(times)
        html_string=BeautifulSoup(requests.get(str(url)).text,'html.parser').select("#gz_gszzl")
        v=re.compile(r'(?<=>).*%').findall(str(html_string))[0]            #正则
        t=time.strftime('%Y-%m-%d:%H:%M',time.localtime(time.time()))
        print "%s \t %s \t %s" %(name,v,t)
        sql="INSERT INTO record (Name,Value,nTime) VALUES ('%s','%s','%s')" %(name,v,t)
        conn.execute(sql)
        conn.commit()

address1='http://fund.eastmoney.com/003625.html?spm=search'
address2='http://fund.eastmoney.com/161725.html?spm=search'

if __name__ == '__main__':
    createdb(name=db_name)
    pool = multiprocessing.Pool(processes = 3)
    while True:
        pool.apply(html_info, (address1,'创金合信资源股票发起式C',2, ))
        pool.apply(html_info, (address2,'招商中证白酒指数分级',2, ))
