#coding=utf-8

import requests
import json

def py():
    url = 'http://fanyi.baidu.com/v2transapi/'
    data={
      'from':'en',
      'to':'zh',
      'query':"captain",        #单词 or 短语
      'transtype':'translang',
      'simple_means_flag':'3'
      }        
    headers ={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0'}
    response = requests.post(url,data,headers=headers)
    head = response.headers
    x=response.json()['trans_result']['data'][0]
    print json.dumps(x).decode("unicode-escape")

if __name__=="__main__":
    py()

    
#官方API文档：http://api.fanyi.baidu.com/api/trans/product/apidoc
