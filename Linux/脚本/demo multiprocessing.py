#!/usr/bin/env python
#encoding:utf8

#demo1
from multiprocessing import Process
import time,os
def f(name):
    time.sleep(1)
    print 'hello ',name
    print os.getppid()   # 取得父进程ID
    print os.getpid()    # 取得进程ID
process_list = []

for i in range(10):
    p = Process(target=f,args=(i,))
    p.start()
    process_list.append(p)
for j in process_list:
    j.join()
    
#demo2 
from multiprocessing import Pool
import time,os
def f(name):
    time.sleep(1)
    print 'hello ',name
    print os.getppid()
    print os.getpid()
process_list = []

pool = Pool(4)
res = pool.map(f, range(1,10))
pool.close()
pool.join()

#demo3 (进程间通信)
from multiprocessing import Process,Queue
import time
def f(name):
    time.sleep(1)
    q.put(['hello'+str(name)])
process_list = []
q = Queue()
if __name__ == '__main__':
    for i in range(10):
        p = Process(target=f,args=(i,))
        p.start()
        process_list.append(p)
    for j in process_list:
        j.join()
    for i in range(10):
        print q.get()

#demo4 (同步)
from multiprocessing import Process,Lock
import time
import os

def f(name):
    lock.acquire()    #加锁,使某一时刻只有一个进程,其他在调用同一个锁就会被阻塞
    time.sleep(1)
    print 'hello--'+str(name)
    print os.getppid(),'-----------',os.getpid()
    lock.release()
process_list = []
lock = Lock()
if __name__ == '__main__':
    for i in range(10):
        p = Process(target=f,args=(i,))
        p.start()
        process_list.append(p)
    for j in process_list:
        j.join()
 
 #demo5 (进程池)
import multiprocessing
import time,os

result = []
def run(h):
    print 'threading:' ,h,os.getpid()
p = multiprocessing.Pool(processes=20)

for i in range(100):
    result.append(p.apply_async(run,(i,)))
p.close()

for res in result:
    res.get(timeout=5)
    
    
