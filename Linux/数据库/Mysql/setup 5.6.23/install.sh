#!/bin/bash

mysql_home="/usr/local/mysql"
mysql_sock="/var/lib/mysql/mysql.sock"
data="/data"

set -e
set -x

#身份检查
if [ $(id -u) != "0" ]; then
    echo "error: user must be an administrator"
    exit;
fi

#准备目录
mkdir -p $mysql_home/etc
mkdir -p $data
mkdir -p $(dirname $mysql_sock)

#依赖
yum -y install gcc gcc-c++ ncurses-devel cmake mysql perl-Module-Install.noarch

#已经下载到了同级目录
#wget http://dev.mysql.com/get/Downloads/MySQL-5.6/mysql-5.6.23.tar.gz

tar -zxf mysql-5.6.23.tar.gz
chown root:root mysql-5.6.23
cd mysql-5.6.23
cmake . \
-DCMAKE_INSTALL_PREFIX=$mysql_home \
-DSYSCONFDIR=$mysql_home/etc \
-DMYSQL_DATADIR=$data \
-DMYSQL_UNIX_ADDR=$mysql_sock \
-DWITH_INNOBASE_STORAGE_ENGINE=1 \
-DENABLED_LOCAL_INFILE=1 \
-DMYSQL_TCP_PORT=3306 \
-DEXTRA_CHARSETS=all \
-DDEFAULT_CHARSET=utf8 \
-DDEFAULT_COLLATION=utf8_general_ci \
-DWITH_DEBUG=0
make
make install

#用户
groupadd mysql
useradd -r -g mysql -s /sbin/nologin mysql 
chown -R mysql:mysql $data

cd $mysql_home
scripts/mysql_install_db --user=mysql --datadir=$data

#备份旧的配置
mkdir etc
[ -f "/etc/my.cnf" ] &&  mv /etc/my.cnf /etc/my.cnf.bak
cp support-files/my-default.cnf /etc/my.cnf
cp support-files/mysql.server /etc/init.d/mysqld
chmod 755 /etc/init.d/mysqld

/etc/init.d/mysqld start

./bin/mysql_secure_installation

exit 0