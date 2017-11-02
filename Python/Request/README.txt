#!/usr/bin/env python

# 官方中文文档 http://cn.python-requests.org/zh_CN/latest/user/quickstart.html#id2
# need sudo pip install requests
import requests

# get方法提交表单
url = r'http://dict.youdao.com/search?le=eng&q={0}'.format(word.strip())
r = requests.get(url,timeout=2)

# get方法带参数 http://httpbin.org/get?key=val
r = requests.get("http://httpbin.org/get", params={'key1': 'value1', 'key2': 'value2'})

# post方法提交表单
QueryAddress='http://www.anti-spam.org.cn/Rbl/Query/Result'
r = requests.post(url=QueryAddress, data={'IP':'211.211.54.54'})

# 定制请求头post请求
headers = {'content-type': 'application/json'}
r = requests.post(url, data=json.dumps({'some': 'data'}), headers=headers)

# 复杂post请求
url = 'http://m.ctrip.com'
payload = {'some': 'data'}
r = requests.post(url, data=json.dumps(payload)) #如果传递的payload是string而不是dict，需要先调用dumps方法格式化一下

# https登录加auth
r = requests.get('https://baidu.com', auth=('user', 'pass'))

# 判断请求是否正常
if r.ok:    
    print r.url             # u'http://httpbin.org/get?key2=value2&key1=value1'
    print r.status_code     # 状态码
    print r.content         # 获取到的原始内容  可使用 BeautifulSoup4 解析处理判定结果
    print r.text            # 把原始内容转unicode编码
    print r.headers         # 响应头
    print r.headers['content-type']          # 网页头信息 不存在为None
    print r.cookies['example_cookie_name']   # 查看cookie
    print r.history         # 追踪重定向 [<Response [301]>]  开启重定向 allow_redirects=True

# 获取，修改网页编码
r = requests.get('https://github.com/timeline.json')
print r.encoding
r.encoding = 'utf-8'

# 设置超时时间
r = requests.get('http://m.ctrip.com', timeout=0.001)

# 获取JSON
r = requests.get('https://github.com/timeline.json')
r.json()

# 获取图片
from PIL import Image
from StringIO import StringIO
i = Image.open(StringIO(r.content))

# 发送cookies到服务器
url = 'http://httpbin.org/cookies'
cookies = dict(cookies_are='working')
r = requests.get(url, cookies=cookies)
print r.text                # >>> '{"cookies": {"cookies_are": "working"}}'

# 在同一个Session实例发出的所有请求之间保持cookies
s = requests.session()
login_data = {'email': '***', 'password': '***', }
s.post('http://www.zhihu.com/login', login_data)
r = s.get('http://www.zhihu.com')

# 会话对象能够跨请求保持某些参数
s = requests.Session()
s.auth = ('user', 'pass')
s.headers.update({'x-test': 'true'})
s.get('http://httpbin.org/headers', headers={'x-test2': 'true'})  # both 'x-test' and 'x-test2' are sent

# ssl证书验证
requests.get('https://github.com', verify=True)
requests.get('https://kennethreitz.com', verify=False)   #忽略证书验证
requests.get('https://kennethreitz.com', cert=('/path/server.crt', '/path/key')) #本地指1个证书 正确 200 错误 SSLError

# 流式上传
with open('massive-body') as f:
    requests.post('http://some.url/streamed', data=f)

# 流式请求
import requests
import json
r = requests.post('https://stream.twitter.com/1/statuses/filter.json', \
    data={'track': 'requests'}, \
    auth=('username', 'password'), \
    stream=True)
for line in r.iter_lines():
    if line: # filter out keep-alive new lines
    print json.loads(line)

# 自定义身份验证
from requests.auth import AuthBase
class PizzaAuth(AuthBase):
    """Attaches HTTP Pizza Authentication to the given Request object."""
    def __init__(self, username):
        # setup any auth-related data here
        self.username = username
    def __call__(self, r):
        # modify and return the request
        r.headers['X-Pizza'] = self.username
        return r
requests.get('http://pizzabin.org/admin', auth=PizzaAuth('kenneth'))

# 基本身份认证
from requests.auth import HTTPBasicAuth
requests.get('https://api.github.com/user', auth=HTTPBasicAuth('user', 'pass'))

# 摘要式身份认证
from requests.auth import HTTPDigestAuth
url = 'http://httpbin.org/digest-auth/auth/user/pass'
requests.get(url, auth=HTTPDigestAuth('user', 'pass'))

# 代理
import requests
proxies = {
  "http": "http://10.10.1.10:3128",
  # "http": "http://user:pass@10.10.1.10:3128/",  # 用户名密码
  "https": "http://10.10.1.10:1080",
}
requests.get("http://example.org", proxies=proxies)
#也可设置环境变量之间访问
export HTTP_PROXY="http://10.10.1.10:3128"
export HTTPS_PROXY="http://10.10.1.10:1080"

