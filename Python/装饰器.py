#encoding:utf-8

def log(func):
    def wrapper(*args,**kw):
        print "Testing..."
        return func(*args,**kw)
    return wrapper

@log
def function(x,y):
    print x*y

function(10,10)    
#输出
print "Testing..."
100

#---------------------------------------------------

def log(argument):
    def wrapper_func(func):
        def wrapper_args(*args,**kw):
            print argument
            return func(*args,**kw)
        return wrapper_args
    return wrapper_func

@log('Testing...')
def function(x,y):
    print x*y

function(10,10) 

#---------------------------------------------------

#在类的外部定义一个类的装饰器对类方法进行装饰并使其能够调用类中的其他方法
def catch_exception(func):
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception:
            self.revive()   #不用顾虑，直接调用原来的类的方法
            return 'an Exception raised.'
    return wrapper


class Test(object):
    def __init__(self):
        pass

    def revive(self):
        print('revive from exception.')
        # do something to restore

    @catch_exception
    def read_value(self):
        print('here I will do something.')
        # do something.
        
"""
关于装饰器的具体概念：
http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/001386819879946007bbf6ad052463ab18034f0254bf355000
"""
