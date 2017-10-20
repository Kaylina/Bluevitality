# mysql 多实例status监控脚本

[root@db02 ~]# cat 12-mysql.sh
#!/bin/bash
. /etc/rc.d/init.d/functions

allport=(
3306
3307
3308
)

mysqld="/data/3309/mysql start"
prog="mysqld" 

pid=($(pidofproc mysqld))
port=($(ps -ef|grep -Po 'port=\K\d+'))

rh_status(){
  for ((i=0;i<${#port[@]};i++))
    do
      allport=(${allport[@]#*${port[i]}*})
    done
  success;echo "mysqld (port ${port[@]}) is running..."
  if ! strstr "`echo ${allport[@]}`" "33" ;then
    echo "mysql is ok"
    exit 0
  fi
  failure;echo "mysqld (port ${allport[@]}) is stopped"

while true 
do
  for  n in ${allport[@]}
    do
      echo "Start mysql at $n"
      /data/$n/mysql start
      sleep 4
      if [ `netstat -lntup|grep $n|wc -l` -eq 1 ];then
        allport=(${allport[@]#*$n*})
        success ; echo "mysqld (port $n) success."
         if ! strstr "`echo ${allport[@]}`" "33" ;then
            echo "mysql is ok"
            exit 0
        fi
        fi
      
    done
done
}


case "$1" in
    status)
        rh_$1
        ;;
esac


