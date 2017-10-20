#!/bin/bash

#��������Ŀ¼
DB_BACKUP_DIR="/data/db_backup"
[[ ! -d $DB_BACKUP_DIR ]] && mkdir -p $DB_BACKUP_DIR

#�������ݿ��ʺż�����
DB_USER="root"
DB_PWD="paybay123"

#�������ݿ�
DB_CONNECT="/usr/local/mysql/bin/mysql -hlocalhost -u${DB_USER} -p${DB_PWD}"

#���ݴӿ�ʱʹ��......
#DB_DUMP_CONNECT="/usr/local/mysql/bin/mysqldump -hlocalhost -u${DB_USER} -p${DB_PWD} --dump-slave=2"

#����ʹ��innodb��������ݿⲢ�����м����������־�ı�����ʼ�㣨���鿪�� --flush-logs/-F ������������������־��
DB_DUMP_CONNECT="/usr/local/mysql/bin/mysqldump -hlocalhost -u${DB_USER} -p${DB_PWD} --single-transaction --master-data=2"

#�ų�mysql�Դ������ݿ�
DB_ARRAY=(`${DB_CONNECT} -N  -e "show databases" | grep -Ev "information_schema|mysql|performance_schema"`)
#echo ${DB_ARRAY[@]}

#����ʣ������������������ݿ�
for db in ${DB_ARRAY[@]}
do
    backup_time=`date +%Y%m%d`
    #���ݸ�ʽ������.ʱ��.sql
    ${DB_DUMP_CONNECT} $db > ${DB_BACKUP_DIR}/$db.${backup_time}.sql
done

#ɾ������ʱ�䳬��30��Ŀ�
find $DB_BACKUP_DIR/ -type f -mtime +30 -exec rm -f {} \;