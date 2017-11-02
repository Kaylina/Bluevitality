#!/bin/bash


NGINX_HOME="/usr/local/nginx"
NGINX_CONF="/etc/nginx/nginx.conf"
PERE_HOME="/usr/local/pcre-8.41"
OPENSSL_HOME="/usr/local/openssl-1.0.21"

set -e
set -x

#身份检查   
if [ $(id -u) != "0" ]; then
    echo "error: user must be an administrator"
    exit;
fi

#创建用户
if ! id nginx &> /dev/null ; then
    groupadd nginx
    useradd -M -g nginx  nginx -s /sbin/nologin
fi

#依赖
yum -y install gcc gcc-c++ zlib-devel make

function _install() {
    #yum -y install openssl-devel pcre-devel
    wget -c https://www.openssl.org/source/openssl-1.0.2l.tar.gz && \
    wget -c ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-8.41.tar.gz && \
    wget -c http://nginx.org/download/nginx-1.12.1.tar.gz
    return 0
}

#_install || exit 1

#本地安装
[[ -e "nginx-1.12.1.tar.gz" && -e "openssl-1.0.2l.tar.gz" && -e "pcre-8.41.tar.gz" ]] || exit 1
rm -rf {nginx-1.12.1,openssl-1.0.2l,pcre-8.41,$NGINX_HOME,$NGINX_CONF,$PERE_HOME,$OPENSSL_HOME}

#Openssl
p=$(pwd)
tar zxf openssl-1.0.2l.tar.gz
cd openssl-1.0.2l/
./config --prefix=${OPENSSL_HOME:='/usr/local/openssl-1.0.21'}
make
make install

#PCRE
cd $p
tar zxf pcre-8.41.tar.gz
cd pcre-8.41
./configure --prefix=${PERE_HOME:='/usr/local/pcre-8.41'}
make
make install

#Nginx( pcre & openssl 指向源码的Makefile所在路面，非安装目录..)
cd $p
tar zxf nginx-1.12.1.tar.gz
mkdir -p ${NGINX_HOME}
cd nginx-1.12.1/
./configure  \
--prefix=${NGINX_HOME:='/usr/local/nginx'} \
--conf-path=${NGINX_CONF:-/usr/local/nginx/nginx.conf} \
--sbin-path=${NGINX_HOME:-'/usr/local/nginx'}/sbin/nginx \
--pid-path=/usr/local/nginx/nginx.pid \
--with-http_stub_status_module \
--with-http_gzip_static_module \
--with-pcre=../pcre-8.41 \
--with-openssl=../openssl-1.0.2l \
--with-http_ssl_module
NUM=$( awk '/processor/{NUM++};END{print NUM}' /proc/cpuinfo )
if [ $NUM -gt 1 ] ;then
    make -j $NUM
else
    make
fi
make install

#启动
chmod u+s ${NGINX_HOME:='/usr/local/nginx'}/sbin/nginx
ln -sv ${NGINX_HOME:='/usr/local/nginx'}/sbin/nginx /sbin/nginx

nginx -t
nginx

exit 0
