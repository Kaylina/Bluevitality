#encoding:utf-8

def log(func):
    def wrapper(*args,**kw):
        print "Testing..."
        return func(*args,**kw)
    return wrapper

@log
def function(x,y):
    print x*y

function(10,10)    #输出100

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

function(10,10)     #输出100

#---------------------------------------------------

# 定义一个装饰器
def mydecorator(func):
    def wrapper(*args,**kw):
        print('hi,now is:')
        return func(*args,**kw)
    return wrapper

# 使用装饰器
@mydecorator
def now():
    print('2015-12-9')

now()

#---------------------------------------------------

#在类的外部定义一个类的装饰器对类方法进行装饰并使其能够调用类中的其他方法
def catch_exception(origin_func):
    def wrapper(self, *args, **kwargs):
        try:
            u = origin_func(self, *args, **kwargs)
            return u
        except Exception:
            self.revive() #不用顾虑，直接调用原来的类的方法
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
