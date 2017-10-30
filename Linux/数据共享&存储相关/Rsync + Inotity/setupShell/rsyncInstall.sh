#!/bin/bash

# Check if user is root
if [ $(id -u) != "0" ]; then
    printf "Error: You must be root to run this script!\n"
    exit 1
fi

#检查源码包是否存在
if [ ! -f rsync-3.1.1.tar.gz ]; then
    printf "Error: rsync-3.1.1.tar.gz not found!\n"
    exit 1
fi

#若已存在解压的源码目录先删除
if [ -s rsync-3.1.1 ]; then
    rm -rf rsync-3.1.1
fi

#解压安装
printf "\nInstall Rsync ...\n\n"
tar zxvf rsync-3.1.1.tar.gz
cd rsync-3.1.1
./configure --prefix=/usr/local/rsync
make
make install
cd -

#检查是否存在可执行文件
if [ ! -f /usr/local/rsync/bin/rsync ]; then
    printf "Error: rsync compile install failed!\n"
    exit 1
fi

#创建配置目录和日志目录
mkdir -p /usr/local/rsync/etc
mkdir -m 0777 -p /usr/local/rsync/logs

#创建认证文件
echo "#username:password" > /usr/local/rsync/etc/rsyncd.pass
chmod 600 /usr/local/rsync/etc/rsyncd.pass

#检查若有配置文件先备份
if [ -s /usr/local/rsync/etc/rsyncd.conf ]; then
    mv /usr/local/rsync/etc/rsyncd.conf /usr/local/rsync/etc/rsyncd.conf.bak
fi

#导入配置
cat >/usr/local/rsync/etc/rsyncd.conf<<EOF
uid = nobody
gid = nobody
port = 873
use chroot = yes
max connections = 100
pid file = /var/run/rsyncd.pid
log file = /usr/local/rsync/logs/rsyncd.log
list = no
strict modes = no
secrets file = /usr/local/rsync/etc/rsyncd.pass
ignore errors

#hosts allow = 10.50.201.217
hosts deny=*

#[demo]
#uid = root
#gid = root
#path = /rsync module path
#auth users = username
#read only = no 

EOF

rsync --daemon --config=/usr/local/rsync/etc/rsyncd.conf

#写入启动文件
mv ../rsync.rcd.txt /etc/init.d/rsyncd
chmod 0755 /etc/init.d/rsyncd

#检查是否开机自启，若不存在则写入/etc/rc.local
isSet=`grep "/usr/local/rsync/bin/rsync --daemon" /etc/rc.local | wc -l`
if [ "$isSet" == "0" ]; then
    echo "/usr/local/rsync/bin/rsync --daemon --config=/usr/local/rsync/etc/rsyncd.conf">>/etc/rc.local
fi

service rsyncd restart

printf "\nRsync is running ...\n\n"
ps aux | grep rsync | grep -v "grep"
