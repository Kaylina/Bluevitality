#!/usr/bin/env python


# 打印出独立IP，并统计独立IP数
# 219.140.190.130 - - [23/May/2006:08:57:59 +0800] "GET /fg172.exe HTTP/1.1" 200 2350253
# 221.228.143.52 - - [23/May/2006:08:58:08 +0800] "GET /fg172.exe HTTP/1.1" 206 719996
# 221.228.143.52 - - [23/May/2006:08:58:08 +0800] "GET /fg172.exe HTTP/1.1" 206 713242

dic={}
a=open("a").readlines()
for i in a:
    ip=i.strip().split()[0]
    if ip in dic.keys():
        dic[ip] = dic[ip] + 1
    else:
        dic[ip] = 1
for x,y in dic.items():
    print x," ",y
    
    
