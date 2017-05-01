#coding=utf-8


class student(object):                  #新式类
    '''类的注释用特殊方法__doc__访问'''
    count='此处定义类属性...'
    
    def __init__(self,name,age):        #类的构造函数，进行对实例的初始化操作
        self.__name=name                #定义两个不可以被直接访问的实例变量
        self.__age=age

    def __speak(self,word='default'):               #定义了一个私有化函数，它不可被直接访问
        print "my name is %s , my age is %s" %(self.__name,self.__age)
        print word

    def student_info(self):print "I'm Good boy"

class bad_student(student):                         #继承父类
    '''此处继承父类并重构student_info方法'''
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
