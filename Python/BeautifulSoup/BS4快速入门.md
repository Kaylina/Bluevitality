```python
import urllib 
import urllib.request as request
import re
from bs4 import *
 
url = 'http://www.0756fang.com/'
html = request.urlopen(url).read().decode('utf-8')      #获取网页内容并读取后解码为UTF8格式

soup = BeautifulSoup(html,"html.parser")                #soup方法的第二个参数指定了使用什么解析器
print(soup.head.meta['content'])                        #输出所得标签属性值

print(soup.span.string)                                 #返回标签的text
print(soup.span.text)                                   #两个效果一样，返回标签的text

print(soup.find_all(attrs={'name':'keywords'})) #attrs方法搜索name属性是‘’的标签的<ResultSet>类，是由<Tag>组成的list
print(soup.find_all(class_='site_name'))                #class属性是‘’的<Tag>的list,即<ResultSet>
print(soup.find_all(class_='site_name')[0])             #这是一个<Tag>
 
print(soup.find(attrs={'name':'keywords'}))             #name属性是‘’的标签的<Tag>类
print(soup.find('meta',attrs={'name':'keywords'}))      #name属性是‘’的meta标签的<Tag>类
print(soup.find('meta',attrs={'name':'keywords'})['content'])   #<Tag类>可直接查属性值

#配合re模块使用，可以忽略大小写
#如下面例子，可以找到name属性为keywords，KEYWORDS,KeyWORds等的meta标签
print(soup.find('meta',attrs={'name':re.compile('keywords',re.IGNORECASE)}))

'''----------------------------修改BeautifulSoup—----------------------------'''

soup.find(attrs={'name':'keywords'}).extract    #调用这个方法，可以删除这一个标签
soup.title.name='ppp'                           #把Tag的名字<title>改成<ppp>
 
#可用append(),insert(),insert_after()或insert_before()等方法来对新标签进行插入

Tag1 = a.new_tag('li',class_='123')             '''创造一个Tag'''
a.title.append（Tag1）                          #把Tag1添加为name是title的Tag的最后一个【子节点】，没有换行
      #.insert(0,Tag1)----这里用insert的话，第一个参数可以控制所添加【子节点】的先后位置
      #.insert_after(Tag1)---和insert_before一样，添加为Title的【兄弟节点】
 
soup.head.meta['content']=''                    #随便输入，可以添加（或更改）这个Tag的content属性（值）'
del soup.head.meta['content']                   #这个语法可以直接删除这个Tag的content属性
 
 
soup.li.clear#调用方法会清除所有li标签的text
soup.title.string='用这个方法可以修改title标签的内容'   #慎用，只用于最子孙最小的节点，用于父节点会清空子节点
soup.div.append('放在div子节点位置的 最后append最后，是标签内容')
soup.div.insert(0,'放在div子节点位置的 最前insert【0】最前，是标签内容'')
```

#### 一些例子

```
html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>
<p class="story"><a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>
and they lived at the bottom of a well.</p>
<p class="story">...</p>
""""

find_all(name, attrs, recursive, text, limit, **kwargs)

#举例说明：
print soup.find_all('title')
print soup.find_all('p','title')
print soup.find_all('a')
print soup.find_all(id="link2")
print soup.find_all(id=True)
#返回值为：
[<title>The Dormouse's story</title>]
[<p class="title"><b>The Dormouse's story</b></p>]
[<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>, <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>, <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]
[<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>]
[<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>, <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>, <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]

#通过css查找,直接上例子把：
print soup.find_all("a", class_="sister")
print soup.select("p.title")

#通过属性进行查找
print soup.find_all("a", attrs={"class": "sister"})

#通过文本进行查找
print soup.find_all(text="Elsie")
print soup.find_all(text=["Tillie", "Elsie", "Lacie"])

#限制结果个数
print soup.find_all("a", limit=2)

#搜索tag名 <title></title>
soup.find_all("title")

#搜索id为"link2"的标签
soup.find_all(id='link2')

#这里属性的值可以使用字符串,正则表达式 ,列表,True
soup.find_all(id=re.compile("elsie"))

#可以指定多个条件
soup.find_all(href=re.compile("elsie"), id='link1')

#对于有些不能指定的标签(data-foo)
soup.find_all(attrs={"data-foo": "value"})

#对于class -->class为python保留字使用class_
soup.find_all(class_="top")

#基础 内容为'Elsie'的
soup.find_all(string="Elsie")

#内容在数组中的
soup.find_all(string=["Tillie", "Elsie", "Lacie"])

#内容匹配正则表达式的
soup.find_all(string=re.compile("Dormouse"))

#匹配函数
soup.find_all(string=is_the_only_string_within_a_tag)#搜索tag为title
soup.select("title")

#通过tag标签逐层查找
soup.select("html head title")

#寻找直接子标签
soup.select("head > title")
soup.select("p > #link1")

#选择所有紧接着id为link1元素之后的class为sister的元素
soup.select("#link1 + .sister")

#选择p元素之后的每一个ul元素
soup.select("p + ul")

#同时用多种CSS选择器查询元素
soup.select("#link1,#link2")

#通过查询元素属性
soup.select('a[href="http://example.com/elsie"]')
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>]

soup.select('a[href^="http://example.com/"]')
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
#  <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>,
#  <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]

soup.select('a[href$="tillie"]')
# [<a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]

soup.select('a[href*=".com/el"]')
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>]
#通过查询元素属性结束

#通过语言查找
soup.select('p[lang|=en]')

#查找第一个元素
soup.select_one(".sister")

#限制搜索数量为2
soup.find_all("a", limit=2)

#只搜索直接子节点
soup.html.find_all("a", recursive=False)

#搜索tag为title
soup.select("title")

#通过tag标签逐层查找
soup.select("html head title")

#寻找直接子标签
soup.select("head > title")
soup.select("p > #link1")

#选择所有紧接着id为link1元素之后的class为sister的元素
soup.select("#link1 + .sister")

#选择p元素之后的每一个ul元素
soup.select("p + ul")

#同时用多种CSS选择器查询元素
soup.select("#link1,#link2")

#通过查询元素属性
soup.select('a[href="http://example.com/elsie"]')
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>]

soup.select('a[href^="http://example.com/"]')
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
#  <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>,
#  <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]

soup.select('a[href$="tillie"]')
# [<a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]

soup.select('a[href*=".com/el"]')
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>]

#通过语言查找
soup.select('p[lang|=en]')

#查找第一个元素
soup.select_one(".sister")
```


