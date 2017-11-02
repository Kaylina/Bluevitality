#!/usr/bin/env python
#coding:utf-8

import paramiko
import sys
import os

#执行命令 demo1
hostname = ''
username = ''
password = ''
paramiko.util.log_to_file('syslogin.log')               # 发送paramiko日志到syslogin.log文件
ssh = paramiko.SSHClient()                              # 创建ssh客户端client对象
ssh.load_system_host_keys()                             # 获取客户端host_keys,默认~/.ssh/know_hosts,非默认路径需指定
ssh.connect(hostname = hostname, username = username, password = password)
stdin, stdout, stderr = ssh.exec_command('free -m')
print stdout.read()
ssh.close()

#执行命令 demo2
host = '10.152.15.200'
user = 'peterli'
password = '123456'

s = paramiko.SSHClient()                                 # 绑定实例
s.load_system_host_keys()                                # 加载本地HOST主机文件
s.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 允许连接不在know_hosts文件中的主机
s.connect(host,22,user,password,timeout=5)               # 连接远程主机
while True:
        cmd=raw_input('cmd:')
        stdin,stdout,stderr = s.exec_command(cmd)        # 执行命令
        cmd_result = stdout.read(),stderr.read()         # 读取命令结果
        for line in cmd_result:
                print line,
s.close()

#执行命令 demo3 (私钥)
host = '10.152.15.123'
user = 'peterli'

s = paramiko.SSHClient()
s.load_system_host_keys()
s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
privatekeyfile = os.path.expanduser('~/.ssh/id_rsa')             # 定义key路径
mykey = paramiko.RSAKey.from_private_key_file(privatekeyfile)
# mykey=paramiko.DSSKey.from_private_key_file(privatekeyfile,password='061128')   # DSSKey方式 password是key的密码
s.connect(host,22,user,pkey=mykey,timeout=5)
cmd=raw_input('cmd:')
stdin,stdout,stderr = s.exec_command(cmd)
cmd_result = stdout.read(),stderr.read()
for line in cmd_result:
        print line,
s.close()

#传输文件
host='127.0.0.1'
port=22
username = 'peterli'
password = '123456'

ssh=paramiko.Transport((host,port))
privatekeyfile = os.path.expanduser('~/.ssh/id_rsa')
mykey = paramiko.RSAKey.from_private_key_file( os.path.expanduser('~/.ssh/id_rsa'))   # 加载key 不使用key可不加
ssh.connect(username=username,password=password)           # 连接远程主机 使用key把 password=password 换成 pkey=mykey
sftp=paramiko.SFTPClient.from_transport(ssh)               # SFTP使用Transport通道
sftp.get('/etc/passwd','pwd1')                             # 下载 两端都要指定文件名
sftp.put('pwd','/tmp/pwd')                                 # 上传
sftp.close()
ssh.close()

# 并发执行
import multiprocessing
import sys,os,time
import paramiko

def ssh_cmd(host,port,user,passwd,cmd):
    msg = "-----------Result:%s----------" % host

    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        s.connect(host,22,user,passwd,timeout=5)
        stdin,stdout,stderr = s.exec_command(cmd)

        cmd_result = stdout.read(),stderr.read()
        print msg
        for line in cmd_result:
                print line,

        s.close()
        except paramiko.AuthenticationException:
            print msg
            print 'AuthenticationException Failed'
        except paramiko.BadHostKeyException:
            print msg
            print "Bad host key"

result = []
p = multiprocessing.Pool(processes=20)
cmd=raw_input('CMD:')
f=open('serverlist.conf')
list = f.readlines()
f.close()
for IP in list:
    print IP
    host=IP.split()[0]
    port=int(IP.split()[1])
    user=IP.split()[2]
    passwd=IP.split()[3]
    result.append(p.apply_async(ssh_cmd,(host,port,user,passwd,cmd)))

p.close()

for res in result:
    res.get(timeout=35)


