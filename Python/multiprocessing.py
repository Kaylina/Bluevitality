#encoding:utf-8

import os
import multiprocessing

def x(x_args):
    while True:
        print str(x_args),os.getpid()

def y(y_args):
    while True:
        print str(y_args),os.getpid()

task=[]
task.append(x)
task.append(y)

if __name__ == '__main__':
    pool=multiprocessing.Pool(processes=len(task))      #或：Pool(multiprocessing.cpu_count())
    num=0
    for i in task:                  #或：for num in xrange(10)
        pool.apply_async(i,(num,))  #非阻塞方式并行执行子进程
        num+=1
    pool.close()    #关闭pool，使其不在接受新的任务
    pool.join()     #主进程暂时阻塞以等待子进程退出

    print 'All subprocesses done.'

    
