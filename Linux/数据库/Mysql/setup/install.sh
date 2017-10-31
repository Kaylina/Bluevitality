#!/bin/bash
services="/usr/local/services"
mysql="/usr/local/services/mysql"
data="/data"
mysqldata="/data/mysql" 

#check runner
if [ $(id -u) != "0" ]; then
    echo "error: user must be an administrator"
    exit;
fi

if [ ! -d "$services" ]; then
    mkdir "$services"
fi
if [ ! -d "$data" ]; then
    mkdir "$data"
fi
if [ ! -d "$mysqldata" ]; then
    mkdir "$mysqldata"
fi

#install cmake & dependence
yum -y install gcc gcc-c++ ncurses-devel cmake
yum -y install perl-Module-Install.noarch

# 先注释，文件已经下载到脚本相同的目录
# wget http://dev.mysql.com/get/Downloads/MySQL-5.6/mysql-5.6.23.tar.gz

tar -zxvf mysql-5.6.23.tar.gz
cd mysql-5.6.23
cmake . -DCMAKE_INSTALL_PREFIX=/usr/local/services/mysql -DSYSCONFDIR=/usr/local/services/mysql/etc -DMYSQL_DATADIR=/data/mysql -DMYSQL_UNIX_ADDR=/data/mysql/mysqld.sock -DWITH_INNOBASE_STORAGE_ENGINE=1 -DENABLED_LOCAL_INFILE=1 -DMYSQL_TCP_PORT=3306 -DEXTRA_CHARSETS=all -DDEFAULT_CHARSET=utf8 -DDEFAULT_COLLATION=utf8_general_ci -DMYSQL_UNIX_ADDR=/data/mysql/mysql.sock -DWITH_DEBUG=0
make
make install

#set after install
groupadd mysql
useradd -r -g mysql mysql
chown -R mysql:mysql /data/mysql/

cd /usr/local/services/mysql/
scripts/mysql_install_db --user=mysql --datadir=/data/mysql

mkdir etc
if [ ! -d "/etc/my.cnf" ]; then
    mv /etc/my.cnf /etc/my.cnf.bak
fi
cp support-files/my-default.cnf etc/my.cnf
cp support-files/mysql.server /etc/init.d/
/etc/init.d/mysql.server start
./bin/mysql_secure_installation

exit 0