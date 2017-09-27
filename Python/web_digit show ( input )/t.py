# -*- coding:utf-8 -*-  

from flask import Flask,render_template,request,redirect,url_for
import time
import copy

app = Flask(__name__)

data=[]

def week(weekday,hour,value):
    if not (weekday <= 8 and weekday >= 0) or not ( hour <= 24 and hour >= 0):
        raise ValueError,'number Error...'
    data.append([weekday-1,hour,value])

@app.route('/',methods=['GET'])
def index():
    for i in range(0,24):   #执行for操作,从数据库读入数据用...
        week(7,i,i*0.9)
    for i in range(1,8):
        if not i == 7:
            week(i,i,i*0.9)
    x=copy.deepcopy(data)
    del data[:]
    return render_template("show.html",list=x)

@app.route('/echarts.js',)
def echarts():
    return render_template("echarts.js")

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
