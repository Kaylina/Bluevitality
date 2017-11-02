#!/usr/bin/env python

from ftplib import FTP
ftp = FTP('ftp.debian.org')                                     # 连接ftp地址   FTP(host,port,timeout)
ftp.login()                                                     # 使用默认anonymous登录  login(user,passwd)
ftp.cwd('debian')                                               # 切换到目录debian
ftp.retrlines('LIST')                                           # 打印目录列表
ftp.retrbinary('RETR README', open('README', 'wb').write)       # 下载文件写到本地
ftp.delete('filename')                                          # 删除ftp中文件
ftp.mkd('dirname')                                              # 在ftp上创建目录
ftp.size('filename')                                            # 查看文件大小
ftp.quit()

