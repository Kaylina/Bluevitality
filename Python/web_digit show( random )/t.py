# -*- coding:utf-8 -*-  

from flask import Flask,render_template,request,redirect,url_for
import random
import os
import time

def week_full(min=1,max=50):
    arry=[]
    for i1 in xrange(0,7):
        for i2 in xrange(0,24):
            digit=int(random.uniform(min, max))
            arry.append([i1,i2,digit])
    return arry

app = Flask(__name__)

@app.route('/',methods=['GET'])
@app.route('/<int:maxi>',methods=['GET'])
def index(maxi=50):
    return render_template("show.html",list=week_full(max=maxi))

@app.route('/echarts.js',)
def r():
    return render_template("echarts.js")

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
