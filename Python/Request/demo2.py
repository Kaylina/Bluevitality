##### 京东商品的爬取--普通爬取框架
```python
import requests  
url = "https://item.jd.com/2967929.html"  
try:  
    r = requests.get(url)  
    r.raise_for_status()  
    r.encoding = r.apparent_encoding  
    print(r.text[:1000])  
except:  
    print("爬取失败！") 
```
#### 亚马逊商品的爬取--通过修改headers字段，模拟浏览器向网站发起请求
```python
import requests  
url="https://www.amazon.cn/gp/product/B01M8L5Z3Y"  
try:  
    kv = {'user-agent':'Mozilla/5.0'}  
    r=requests.get(url,headers=kv)  
    r.raise_for_status()  
    r.encoding=r.apparent_encoding  
    print(r.status_code)  
    print(r.text[:1000])  
except:  
    print("爬取失败")
```
#### 百度/360搜索关键词提交--修改params参数提交关键词
```python
import requests  
url="http://www.baidu.com/s"  
try:  
    kv={'wd':'Python'}  
    r=requests.get(url,params=kv)  
    print(r.request.url)  
    r.raise_for_status()  
    print(len(r.text))  
    print(r.text[500:5000])  
except:  
    print("爬取失败")  
```

#### 网络图片的爬取和存储--结合os库和文件操作的使用
```python
import requests  
import os  
url="http://tc.sinaimg.cn/maxwidth.800/tc.service.weibo.com/p3_pstatp_com/6da229b421faf86ca9ba406190b6f06e.jpg"  
root="D://pics//"  
path=root + url.split('/')[-1]  
try:  
    if not os.path.exists(root):  
        os.mkdir(root)  
    if not os.path.exists(path):  
        r = requests.get(url)  
        with open(path, 'wb') as f:  
            f.write(r.content)  
            f.close()  
            print("文件保存成功")  
    else:  
        print("文件已存在")  
except:  
    print("爬取失败")  
```
