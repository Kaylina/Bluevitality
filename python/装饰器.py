#encoding:utf-8

def log(f):
    def wrapper(*args,**kw):
        print u"无参装饰器..."
        return f(*args,**kw)
    return wrapper

@log
def a(x,y):
    print x*y

a(3,2)  #输出6

#---------------------------------------------------

def xy(v):
    def wrapper1(f):
        def wrapper2(*args,**kw):
            print "装饰器参数:%s" %(v)
            return f(*args,**kw)
        return wrapper2
    return wrapper1

@xy('test')
def b(x,y):
    print x*y

b(3,6)  #输出18
