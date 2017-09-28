
#### HTTP请求类型
|类型|方法|
|:----:|:----|
|get    | `r = requests.get('https://github.com/timeline.json')`|
|post   | `r = requests.post("http://m.ctrip.com/post")`|
|put    | `r = requests.put("http://m.ctrip.com/put")`|
|delete | `r = requests.delete("http://m.ctrip.com/delete")`|
|head   | `r = requests.head("http://m.ctrip.com/head")`|
|options| `r = requests.options("http://m.ctrip.com/get")`|

####获取响应内容
```python
print r.content #以字节的方式去显示，中文显示为字符
print r.text #以文本的方式去显示
```
####URL传递参数
```python
payload = {'keyword': '日本', 'salecityid': '2'}
r = requests.get("http://m.ctrip.com/webapp/tourvisa/visa_list", params=payload) 
print r.url #示例为http://m.ctrip.com/webapp/tourvisa/visa_list?salecityid=2&keyword=日本
```
####获取/修改网页编码
```python
r = requests.get('https://github.com/timeline.json')
print r.encoding
r.encoding = 'utf-8'
```
####json处理
```python
r = requests.get('https://github.com/timeline.json')
print r.json() #需要先import json    
```
####定制请求头
```python
url = 'http://m.ctrip.com'
headers = {'User-Agent' : 'Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 4 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19'}
r = requests.post(url, headers=headers)
print r.request.headers
```
####复杂post请求
```python
url = 'http://m.ctrip.com'
payload = {'some': 'data'}
r = requests.post(url, data=json.dumps(payload)) #如果传递的payload是string而不是dict，需要先调用dumps方法格式化一下
```
####post多部分编码文件
```python
url = 'http://m.ctrip.com'
files = {'file': open('report.xls', 'rb')}
r = requests.post(url, files=files)
```
####响应状态码
```python
r = requests.get('http://m.ctrip.com')
print r.status_code
```
####响应头
```python
r = requests.get('http://m.ctrip.com')
print r.headers
print r.headers['Content-Type']
print r.headers.get('content-type') #访问响应头部分内容的两种方式
```
####Cookies
```python
url = 'http://example.com/some/cookie/setting/url'
r = requests.get(url)
r.cookies['example_cookie_name']    #读取cookies
    
url = 'http://m.ctrip.com/cookies'
cookies = dict(cookies_are='working')
r = requests.get(url, cookies=cookies) #发送cookies
```
####设置超时时间
```python
r = requests.get('http://m.ctrip.com', timeout=0.001)
```
####设置访问代理
```python
proxies = {
           "http": "http://10.10.10.10:8888",
           "https": "http://10.10.10.100:4444",
          }
r = requests.get('http://m.ctrip.com', proxies=proxies)
```

#### json请求
```python
#!/user/bin/env python
#coding=utf-8
import requests
import json

class url_request():
 def __init__(self):
         """ init """    

if __name__=='__main__':
 headers = {'Content-Type' : 'application/json'}
 payload = {'CountryName':'中国',
            'ProvinceName':'陕西省',
            'L1CityName':'汉中',
            'L2CityName':'城固',
            'TownName':'',
            'Longitude':'107.33393',
            'Latitude':'33.157131',
            'Language':'CN'
            }
 r = requests.post("http://www.xxxxxx.com/CityLocation/json/LBSLocateCity",headers=headers,data=paylo
 #r.encoding = 'utf-8'
 data=r.json()
 if r.status_code!=200:
     print "LBSLocateCity API Error " + str(r.status_code)
 print data['CityEntities'][0]['CityID'] #打印返回json中的某个key的value
 print data['ResponseStatus']['Ack']
 print json.dumps(data,indent=4,sort_keys=True,ensure_ascii=False)  #树形打印json，ensure_ascii必须设为False否则中文会显示为unicode
```

#### XML请求
```python
#!/user/bin/env python
#coding=utf-8
import requests

class url_request():
    def __init__(self):
            """ init """    

if __name__=='__main__':
    
    headers = {'Content-type': 'text/xml'}
    XML = '<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><Request xmlns="http://tempuri.org/"><jme><JobClassFullName>WeChatJSTicket.JobWS.Job.JobRefreshTicket,WeChatJSTicket.JobWS</JobClassFullName><Action>RUN</Action><Param>1</Param><HostIP>127.0.0.1</HostIP><JobInfo>1</JobInfo><NeedParallel>false</NeedParallel></jme></Request></soap:Body></soap:Envelope>'
    url = 'http://jobws.push.mobile.xxxxxxxx.com/RefreshWeiXInTokenJob/RefreshService.asmx'
    r = requests.post(url,headers=headers,data=XML)
    #r.encoding = 'utf-8'
    data = r.text
    print data
```

参考:
http://blog.csdn.net/iloveyin/article/details/21444613
http://blog.csdn.net/liuchunming033/article/details/45538205