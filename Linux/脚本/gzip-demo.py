#!/usr/bin/env python


#压缩gzip
File = 'xuesong_18.log'
g = gzip.GzipFile(filename="", mode='wb', compresslevel=9, fileobj=open((r'%s.gz' %File),'wb'))
g.write(open(r'%s' %File).read())
g.close()

#解压gzip
g = gzip.GzipFile(mode='rb', fileobj=open((r'xuesong_18.log.gz'),'rb'))
open((r'xuesong_18.log'),'wb').write(g.read())

