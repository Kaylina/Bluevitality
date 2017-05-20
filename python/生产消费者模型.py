#生产者消费者模型实现多线程异步交互
#coding=utf8
import threading
import time
import Queue
import random

q=Queue.Queue()                #实例化先进先出队列q

def producer(name):

    for i in xrange(1,12):                                  #生产N次
        q.put(i)                                            #生产者向队列q产生包子
        sum=q.qsize
        print "生产者: %s 制作了一个包子：%s ,包子共有：%s 个\n" %(name,i,str(sum))
        time.sleep(random.randrange(2))

def consumer(name):

    count=0
    while count < 5:                                        #消费N次
        time.sleep(random.randrange(1))
        if q.empty():                                       #判断队列是否有数据
            print "包子没了...."
            continue
        data=q.get()                                        #消费者从队列q消费包子
        sum=q.qsize
        print "消费者 %s 消费了一个包子：%s 包子共有：%s 个\n" %(name,data,str(sum))
        count += 1

p=threading.Thread(target=producer,args=('Wy',))
c=threading.Thread(target=consumer,args=('Linux',))
c2=threading.Thread(target=consumer,args=('Linux',))

My_thread=[]
My_thread.append(p)
My_thread.append(c)

for i in My_thread:
    i.start()
