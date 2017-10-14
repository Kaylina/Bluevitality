```python
with open(r'somefileName') as somefile:   #with后面是个表达式，它返回的是一个上下文管理器对象
        for line in somefile:             #使用as可将此结果赋值给某个变量以方便之后操作。
            print line
            # ...more code
            
#使用with后不管with中的代码出现什么错误，都会进行对当前对象进行清理工作
#例如file的file.close()方法，无论with中出现任何错误，都会执行file.close()方法
```

### 说明
with只有特定场合下才能使用，这个特定场合指的是那些支持了上下文管理器的对象  
比如：  
* file  
* decimal.Context  
* thread.LockType  
* threading.Lock  
* threading.RLock  
* threading.Condition  
* threading.Semaphore  
* threading.BoundedSemaphore  

### 什么是上下文管理器

这个管理器就是在对象内实现了两个方法：**__enter__()** 和 **__exit__()**
* __enter__() 在with的代码块执行之前执行  
* __exit__()  在代码块执行结束后执行( 内部会包含当前对象的清理方法 )  
上下文管理器可以自定义，也可以重写__enter__()和__exit__()方法  

with语句类似  
　　try:  
　　except:  
　　finally:  
的功能：但是with语句更简洁。而且更安全。代码量更少。  


### Example
```python
#实现一个类，其含有一个实例属性 db 和上下文管理器所需要的方法 __enter()__ 和 __exit()__ 
class transaction(object):
  def __init__(self, db):
    self.db = db

  def __enter__(self):
    self.db.begin()

  def __exit__(self, type, value, traceback):
    if type is None:
      db.commit()
    else:
      db.rollback()
```
