#!/bin/bash

set -e
set -x

USER="memcached"
MEMCACHED_HOME="/usr/local/memcached"
pidfile="/var/run/memcached.pid"
PORT=11211

#身份检查
if [ $(id -u) != "0" ]; then
	printf "Error: You must be root to run this script!\n"
	exit 1
fi

printf "=== Memcached install start... ===\n\n"

#依赖
if [ ! -f /usr/local/lib/libevent.so ]; then
	if [ -s libevent-2.0.22-stable.tar.gz ]; then
		echo "libevent-2.0.22-stable.tar.gz [found]"
	else
		wget http://jaist.dl.sourceforge.net/project/levent/libevent/libevent-2.0/libevent-2.0.22-stable.tar.gz		
	fi

	[ -s libevent-2.0.22-stable ] && rm -rf libevent-2.0.22-stable
	
	yum -y install gcc gcc-c++	
	tar zxvf libevent-2.0.22-stable.tar.gz
	cd libevent-2.0.22-stable
	./configure --prefix=/usr/local
	make
	make install
	cd -

	if [ ! -f /usr/local/lib/libevent.so ]; then
		printf "Error: libevent compile install failed!\n"
		exit 1
	fi
fi

if [ -s memcached-1.4.24.tar.gz ]; then
	echo "memcached-1.4.24.tar.gz [found]"
else
	wget http://www.memcached.org/files/memcached-1.4.24.tar.gz	
fi

#安装
[ -s memcached-1.4.24 ] && rm -rf memcached-1.4.24
tar zxvf memcached-1.4.24.tar.gz
cd memcached-1.4.24
./configure --prefix=${MEMCACHED_HOME:-/usr/local/memcached} --with-libevent=/usr/local
make
make install
cd -

if [ ! -f /usr/local/memcached/bin/memcached ]; then
	printf "Error: memcached compile install failed!\n"
	exit 1
fi

if [ ! -d /var/run/memcached ]; then
	mkdir -p /var/run/memcached
	chmod 0777 -R /var/run/memcached
fi

#运行身份
groupadd memcached
useradd -g memcached ${USER} -s /bin/nologin

#配置文件
mkdir -p /usr/local/memcached/etc
cat > /usr/local/memcached/etc/memcached.conf <<EOF
PORT="11211"
USER="memcached"
MAXCONN="${PORT:-11211}"
CACHESIZE="256"
OPTIONS="-a 0766 -s /var/run/memcached/memcache.socket"
EOF

cp /usr/local/memcached/bin/memcached /etc/rc.d/init.d/
chmod 0755 /etc/rc.d/init.d/memcached

#demo
#/usr/local/ -d -m 10 -u root -l 127.0.0.0 -p 11211 -c 256 -P ${pidfile}

/etc/rc.d/init.d/memcached -u ${USER} -d start
echo "/etc/rc.d/init.d/memcached -u ${USER} -d  start " >> /etc/rc.local

printf "\n=== Memcached install Completed! ===\n\n"

ps -ef | grep memcached | awk '/start/{print $0}'
