#coding=utf-8

class student(object):
    '''some information ...'''          #类注释用特殊属性__doc__访问
    count='string'                      #类属性（实例共有的）
    
    def __init__(self,name,age):        #构造函数，创建实例时将进行初始化
        self.__name=name                #定义了两个不可以被直接访问的实例变量
        self.__age=age

    def __speak(self,word='default'):               #定义了一个私有化函数，它不可被直接访问
        print "my name is %s , my age is %s" %(self.__name,self.__age)
        print word

    def student_info(self):
        print "I'm Good boy"

    @staticmethod                       #静态方法基本上跟一个全局函数相同，一般来说用的很少
    def sayHello(hi):
        if hi is None:
            hi = 'hello'
        print(hi)

    @classmethod                        #类方法第1个参数是cls，而实例方法的第1个参数是self，表示该类的1个实例
    def hi(cls,msg):
        print(msg)
        print(dir(cls))
		
	@@property							#只读属性装饰器（可以使用正常的点符号访问，但不能对其值进行修改）
	def only_read(self):
		print "{num}".format(num=count,)


class bad_student(student):                         #继承
    '''继承了1个父类并重构student_info方法'''
    def student_info(self):print "I'm Bad boy"      #重构父类方法

for i in range(3):
    number=i
    i=student(i,i+20)
    if number >= 2:
        i._student__speak(word='very hight')        #通过_classname__functionf的形式可访问私有化函数
    else:
        i._student__speak(word='.....')

wy=bad_student('bad_boy',10)
wy.new_variable='value...'              #赋予实例新的变量和值
print wy.new_variable
print student.__doc__                   #输出类注释
print student.count                     #输出类的值
print wy.student_info()

#调用静态方法不用实例化
student.sayHello('hi')
student.hi('Hi!')

#实例化类调用普通方法,__init__在这里触发（python中实现静态方法和类方法都是依赖于python的修饰器来实现的）
person = student()
person.student_info()