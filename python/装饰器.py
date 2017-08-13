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
