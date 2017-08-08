# -*- coding:utf-8 -*-  

import requests
import multiprocessing
from flask import Flask,render_template,request,redirect,url_for
from werkzeug.utils import secure_filename
import os
import re
import time
from bs4 import  BeautifulSoup
import sqlite3

db_name=str(time.strftime('sqlite.'+'%Y-%m',time.localtime(time.time()))+'.db')
conn = sqlite3.connect(db_name,check_same_thread = False)

app = Flask(__name__)

def createdb(name):
    try:
        conn = sqlite3.connect(name)
        conn.execute('''CREATE TABLE record(Name CHAR(10),Value CHAR(50),nTime CHAR(50));''')
        conn.close()
    except: print "already exists %s file..." %(name)
    else:   print "DB name: \t %s" %(str(os.getcwd())+'\\'+name)

def html_info(url,name,times=300):
    global time_value
    while True:
        if str(time.strftime('%H:%S',time.localtime(time.time()))) == "15:02": 
            os.exit()
        html_string=BeautifulSoup(requests.get(str(url)).text,'html.parser').select("#gz_gszzl")
        v=re.compile(r'(?<=>).*%').findall(str(html_string))[0]
        t=time.strftime('%Y-%m-%d:%H:%M',time.localtime(time.time()))
        print "%s \t %s \t %s" %(name,v,t)
        sql="INSERT INTO record (Name,Value,nTime) VALUES ('%s','%s','%s')" %(name,v,t)
        conn.execute(sql)
        conn.commit()
        time.sleep(times)

fs = conn.cursor()

@app.route('/',methods=['GET'])
def index():
    t_list=[]
    v_list=[]
    fs.execute("select * from %s" %('record'))
    for i in fs.fetchall():
        t_list.append(i[2])
        v_list.append(i[1])[半成品！]
    return render_template("show.html",t=t_list,v=v_list)    #包含时间和数值的列表字典！键是time

delay_time=5
Address={}
Address['003625']='http://fund.eastmoney.com/003625.html?spm=search'
Address['161725']='http://fund.eastmoney.com/161725.html?spm=search'

if __name__ == '__main__':
    createdb(name=db_name)
    pool = multiprocessing.Pool(processes=len(Address))
    for key,value in Address.items():
        print "Name: %-20s  URL:%s" %(key,value)
        pool.apply_async(html_info, (value,key,delay_time))
    app.run(host="0.0.0.0",debug=True)
    pool.close()
    pool.join()

