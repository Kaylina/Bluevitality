#!/usr/bin/env python
# nooed pip install python-memcached   # 安装(python2.7+)

import memcache
mc = memcache.Client(['10.152.14.85:12000'],debug=True)    #也可用socket直接连接IP端口
mc.set('name','luo',60)
mc.get('name')
mc.delete('name1')

# 豆瓣的python-memcache模块，大于1M自动切割 性能是纯python的3倍+
# https://code.google.com/p/python-libmemcached/

#保存数据

set(key,value,timeout)              # 把key映射到value，timeout指的是什么时候这个映射失效
add(key,value,timeout)              # 仅当存储空间中不存在键相同的数据时才保存
replace(key,value,timeout)          # 仅当存储空间中存在键相同的数据时才保存

#获取数据
get(key)                            # 返回key所指向的value
get_multi(key1,key2,key3)           # 可以非同步地同时取得多个键值， 比循环调用get快数十倍


