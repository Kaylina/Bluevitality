#!/usr/bin/env python
#encoding:utf-8
#sudo pip install BeautifulSoup

import requests
from BeautifulSoup import BeautifulSoup
import re

baseurl = 'http://blog.sina.com.cn/s/articlelist_1191258123_0_1.html'

r = requests.get(baseurl)

for url in re.findall('<a.*?</a>', r.content, re.S):
    if url.startswith('<a title='):
        with open(r'd:/final.txt', 'ab') as f:
            f.write(url + '\n')

linkfile = open(r'd:/final.txt', 'rb')
soup = BeautifulSoup(linkfile)
for link in soup.findAll('a'):
    #print link.get('title') + ':    ' + link.get('href')
    ss = requests.get(link.get('href'))
    for content in re.findall('<div id="sina_keyword_ad_area2" class="articalContent  ">.*?</div>', ss.content, re.S):
        with open(r'd:/myftp/%s.txt'%link.get('title').strip('<>'), 'wb') as f:
            f.write(content)
            print '%s   has been copied.' % link.get('title')
           
           
