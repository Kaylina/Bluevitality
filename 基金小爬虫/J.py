# -*- coding:utf-8 -*-  

import requests
import multiprocessing
from flask import Flask,render_template,request,redirect,url_for
from werkzeug.utils import secure_filename
from bs4 import  BeautifulSoup
import sqlite3
import os
import re
import time

db_name=str(time.strftime('sqlite.'+'%Y-%m',time.localtime(time.time()))+'.db')     #数据库按月分割
conn = sqlite3.connect(db_name,check_same_thread = False)

def createdb(name):
    try:
        conn = sqlite3.connect(name)
        conn.execute('''CREATE TABLE record(Name CHAR(10),Value CHAR(50),nTime CHAR(50));''')
        conn.close()
    except: print "already exists %s file..." %(name)
    else:   print "DB name: \t %s" %(str(os.getcwd())+'\\'+name)

def html_info(url,name,times=300):
    while True:
        if str(time.strftime('%H:%S',time.localtime(time.time()))) == "15:02": 
            os.exit()
        html_string=BeautifulSoup(requests.get(str(url)).text,'html.parser').select("#gz_gszzl")
        v=re.compile(r'(?<=>).*(?=%)').findall(str(html_string))[0]
        t=time.strftime('%d-%H:%M',time.localtime(time.time()))
        print "%s \t %s \t %s" %(name,v,t)
        sql="INSERT INTO record (Name,Value,nTime) VALUES ('%s','%s','%s')" %(name,v,t)
        conn.execute(sql)
        conn.commit()
        time.sleep(times)

fs = conn.cursor()

def export_info(j_type,limit):
    storage=[]
    fs.execute("select DISTINCT nTime,Value,Name  from %s where Name = '%s' limit %d" %('record',str(j_type),int(limit)))
    for i in fs.fetchall():
        if float(i[1]) < 0:
            convert=abs(float(i[1]))
            bad=u''' {y:%.2f,attrs:{fill:'red'}} ''' %convert    #安全转换 -->{{ XXX | safe }}
            storage.append({'time':i[0],'value':bad})
            continue
        storage.append({'time':i[0],'value':float(i[1])})
    return storage

app = Flask(__name__)

@app.route('/')
@app.route('/<int:limit>',methods=['GET'])
def index(limit=100):
    for_num=0
    tmp={}
    for i in Address.keys():
        for_num+=1
        tmp['d'+str(for_num)]=i
        tmp['digit'+str(for_num)]=export_info(str(i),limit)    
    return render_template("show.html",**tmp)

delay_time=300
Address={}
Address['003625']='http://fund.eastmoney.com/003625.html?spm=search'
Address['161725']='http://fund.eastmoney.com/161725.html?spm=search'

if __name__ == '__main__':
    createdb(name=db_name)
    pool = multiprocessing.Pool(processes=len(Address))
    for key,value in Address.items():
        print u"catch!  Name: %-10s  URL:%s" %(key,value)
        pool.apply_async(html_info,(value,key,delay_time))
    app.run(host="0.0.0.0",debug=True)
    pool.close()
    pool.join()
