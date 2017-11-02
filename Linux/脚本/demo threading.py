#!/usr/bin/env python

from Queue import Queue
import random,time,threading

'''
Thread                    # 表示一个线程的执行的对象
    start()               # 开始线程的执行
    run()                 # 定义线程的功能的函数(一般会被子类重写)
    join(timeout=None)    # 允许主线程等待线程结束,程序挂起,直到线程结束;如果给了timeout,则最多等待timeout秒.
    getName()             # 返回线程的名字
    setName(name)         # 设置线程的名字
    isAlive()             # 布尔标志,表示这个线程是否还在运行中
    isDaemon()            # 返回线程的daemon标志
    setDaemon(daemonic)   # 后台线程,把线程的daemon标志设置为daemonic(一定要在调用start()函数前调用)
    # 默认主线程在退出时会等待所有子线程结束。如果希望主不等待子，而在退出时自动结束所有的子线程就需设置子线程为后台线程(daemon)
Lock                      # 锁原语对象
Rlock                     # 可重入锁对象.使单线程可以在此获得已获得了的锁(递归锁定)
Condition                 # 条件变量对象能让一个线程停下来,等待其他线程满足了某个条件.如状态改变或值的改变
Event                     # 通用的条件变量.多个线程可以等待某个事件的发生,在事件发生后,所有的线程都会被激活
Semaphore                 # 为等待锁的线程提供一个类似等候室的结构
BoundedSemaphore          # 与Semaphore类似,只是不允许超过初始值
Time                      # 与Thread相似,只是他要等待一段时间后才开始运行
activeCount()             # 当前活动的线程对象的数量
currentThread()           # 返回当前线程对象
enumerate()               # 返回当前活动线程的列表
settrace(func)            # 为所有线程设置一个跟踪函数
setprofile(func)          # 为所有线程设置一个profile函数
'''

#demo1
class Producer(threading.Thread):
    def __init__(self, t_name, queue):
        threading.Thread.__init__(self, name=t_name)
        self.data=queue
    def run(self):
        for i in range(5):
            print "%s: %s is producing %d to the queue!\n" %(time.ctime(), self.getName(), i)
            self.data.put(i)
            self.data.put(i*i)
            time.sleep(2)
        print "%s: %s finished!" %(time.ctime(), self.getName())

class Consumer(threading.Thread):
    def __init__(self, t_name, queue):
        threading.Thread.__init__(self, name=t_name)
        self.data=queue
    def run(self):
        for i in range(10):
            val = self.data.get()
            print "%s: %s is consuming. %d in the queue is consumed!\n" %(time.ctime(), self.getName(), val)
        print "%s: %s finished!" %(time.ctime(), self.getName())

if __name__ == '__main__':
    queue = Queue()
    producer = Producer('Pro.', queue)
    consumer = Consumer('Con.', queue)
    producer.start()
    consumer.start()
    producer.join()
    consumer.join()

#demo2 (后台线程)
import threading
import time,random

class MyThread(threading.Thread):
    def run(self):
        wait_time=random.randrange(1,10)
        time.sleep(wait_time)
        print "%s will wait %d seconds" % (self.name, wait_time)
        print "%s finished!" % self.name

if __name__=="__main__":
    for i in range(5):
        t = MyThread()
        t.setDaemon(True)    # 设置为后台线程,主线程完成时不等待子线程完成就结束
        t.start()
