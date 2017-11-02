#!/usr/bin/env python

import tarfile
import gzip
import os

# 压缩tar.gz
import os
import tarfile
tar = tarfile.open("/tmp/tartest.tar.gz","w:gz")   # 创建压缩包名
for path,dir,files in os.walk("/tmp/tartest"):     # 递归文件目录
    for file in files:
        fullpath = os.path.join(path,file)
        tar.add(fullpath)                          # 创建压缩包
tar.close()

# 解压tar.gz
import tarfile
tar = tarfile.open("/tmp/tartest.tar.gz")
#tar.extract("/tmp")                               # 全部解压到指定路径
names = tar.getnames()                             # 包内文件名
for name in names:
    tar.extract(name,path="./")                    # 解压指定文件
tar.close()


#压缩gzip
File = 'xuesong_18.log'
g = gzip.GzipFile(filename="", mode='wb', compresslevel=9, fileobj=open((r'%s.gz' %File),'wb'))
g.write(open(r'%s' %File).read())
g.close()

#解压gzip
g = gzip.GzipFile(mode='rb', fileobj=open((r'xuesong_18.log.gz'),'rb'))
open((r'xuesong_18.log'),'wb').write(g.read())




