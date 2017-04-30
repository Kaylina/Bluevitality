#!/bin/bash

#创建备份目录
DB_BACKUP_DIR="/data/db_backup"
[[ ! -d $DB_BACKUP_DIR ]] && mkdir -p $DB_BACKUP_DIR

#定义数据库帐号及密码
DB_USER="root"
DB_PWD="paybay123"

#连接数据库
DB_CONNECT="/usr/local/mysql/bin/mysql -hlocalhost -u${DB_USER} -p${DB_PWD}"

#备份从库时使用......
#DB_DUMP_CONNECT="/usr/local/mysql/bin/mysqldump -hlocalhost -u${DB_USER} -p${DB_PWD} --dump-slave=2"

#备份使用innodb引擎的数据库并在其中加入二进制日志的备份起始点（建议开启 --flush-logs/-F 参数来滚动二进制日志）
DB_DUMP_CONNECT="/usr/local/mysql/bin/mysqldump -hlocalhost -u${DB_USER} -p${DB_PWD} --single-transaction --master-data=2"

#排除mysql自带的数据库
DB_ARRAY=(`${DB_CONNECT} -N  -e "show databases" | grep -Ev "information_schema|mysql|performance_schema"`)
#echo ${DB_ARRAY[@]}

#备份剩余生产环境所需的数据库
for db in ${DB_ARRAY[@]}
do
    backup_time=`date +%Y%m%d`
    #备份格式：库名.时间.sql
    ${DB_DUMP_CONNECT} $db > ${DB_BACKUP_DIR}/$db.${backup_time}.sql
done

#删除备份时间超过30天的库
find $DB_BACKUP_DIR/ -type f -mtime +30 -exec rm -f {} \;
