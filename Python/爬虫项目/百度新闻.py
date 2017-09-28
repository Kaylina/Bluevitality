# -*- coding:utf-8 -*-

import requests
import threading
import re
import os
import time
import sqlite3
from bs4 import  BeautifulSoup

def createdb(name):
    try:
        print "DB name: \t %s" %(str(os.getcwd())+'\\'+name)
        db=sqlite3.connect(name)
        db.execute('''CREATE TABLE record(Time CHAR(60),Value CHAR(200));''')
        db.close()
    except:
        print "Create DB Error..."

time=str(time.strftime('%Y-%m-%d_%H',time.localtime(time.time())))
db_name=str(time+u'.db')
db = sqlite3.connect(db_name)

Drop_word=['财经','文化','娱乐','体育','更多','专题','砺石商业评论','科技先生','财视传媒','砺石商业评论','coolcorp','<span>北京</span>新闻',
'<img alt="" src=""/>','新闻订阅','邮件新闻订阅','地区新闻','历史新闻','新闻免费代码','Android版下载','百家号','个性推荐','iPhone版下载']

def news_info(url):
    info=BeautifulSoup(requests.get(str(url)).text,'html.parser').find_all('a',attrs={'target':'_blank'})
    news_strings_pattern=re.compile(r'(?<=>).*(?=</a)') 
    for i in info:
        x=news_strings_pattern.findall(str(i))
        for new in x:
            if not len(new) < 4:
                if not new in Drop_word: 
                    s=re.sub(r'<br/>','__',new)
                    print s
                    db.execute("insert into record (Time,Value) VALUES ('%s','%s')" %(time,s))
                    db.commit()
                


if __name__ == '__main__':
    createdb(name=db_name)
    news_info(url=u'http://news.baidu.com')
