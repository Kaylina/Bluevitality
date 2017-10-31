#!/bin/bash

mysql_home="/usr/local/mysql"
mysql_root_pass=123456
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

#依赖
yum -y install gcc gcc-c++ ncurses-devel cmake mysql perl-Module-Install.noarch

#已经下载到了同级目录
#wget http://dev.mysql.com/get/Downloads/MySQL-5.6/mysql-5.6.23.tar.gz

tar -zxf mysql-5.6.23.tar.gz
chown root:root mysql-5.6.23
cd mysql-5.6.23
cmake . \
-DCMAKE_INSTALL_PREFIX=$mysql_home \
-DSYSCONFDIR=/etc \
-DMYSQL_DATADIR=$data \
-DMYSQL_UNIX_ADDR=/var/lib/mysql/mysql.sock \
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
useradd -r -c "MySQL Server" -g mysql -s /sbin/nologin mysql 
chown -R mysql:mysql $data

cd $mysql_home
scripts/mysql_install_db  --basedir=/usr/local/mysql --datadir=$data --user=mysql 

#备份旧的配置
[ -f "/etc/my.cnf" ] &&  mv /etc/my.cnf /etc/my.cnf.bak
cp -f support-files/my-default.cnf /etc/my.cnf
cp -f support-files/mysql.server /etc/init.d/mysqld
chmod 755 /etc/init.d/mysqld

#启动
$mysql_home/bin/mysqld_safe --skip-grant-tables &

mysql -h 127.0.0.1  <<eof
UPDATE mysql.user SET password=PASSWORD("${mysql_root_pass:=123456}") WHERE user='root';
eof

ps -ef | grep mysqld | awk '/--skip-grant-tables/{print "kill -9 " $2}' | bash -

/etc/init.d/mysqld start
echo "/etc/init.d/mysqld start" >> /etc/rc.local

exit 0