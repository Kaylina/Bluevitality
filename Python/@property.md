
### 以只读方式访问属性或将操作的结果以属性方式返回
```python
>>> class a(object):
...
...     def __init__(self,name,age):
...             self.name=name
...             self.age=age
...
...     @property
...     def var_sum_values(self):   #返回name+age组成的字串
...             return "%s %s" % (self.name,self.age)
...
>>> c.var_sum_values
'wangyu 20'
>>> c.name="duanyan"
>>> c.varsumvalue
'duanyan 20'
```


### 设置转为只读属性（特性）的函数和对赋值加以判断的属性（函数）
> 广泛应用在类定义中，可让调用者写出简短的代码，同时保证对参数进行必要的检查，可程序运行时就减少了出错的可能性
```python
>>> class Student(object):
...
...     @property
...     def score(self):
...         return self._score
...
... #说明：首先装饰了score方法使其成为getter后接着将刚刚装饰过的score方法的setter属性装饰了此方法，而这个方法的名字与之前的方法名字是一样的
...
...     @score.setter               #格式：之前的被装饰函数名.setter
...     def score(self, value):     #将此赋值并判断的函数转为属性，在对其赋值时进行判断若不符合则抛出异常
...         if not isinstance(value, int):
...             raise ValueError('score must be an integer!')
...         if value < 0 or value > 100:
...             raise ValueError('score must between 0 ~ 100!')
...         self._score = value
...
>>> s = Student()
>>> s.score = 60    # OK，实际转化为s.set_score(60)
>>> s.score         # OK，实际转化为s.get_score()
60
>>> s.score = 9999
Traceback (most recent call last):
  ...
ValueError: score must between 0 ~ 100!
```
