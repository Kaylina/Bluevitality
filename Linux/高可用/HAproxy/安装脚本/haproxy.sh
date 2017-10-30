#!/bin/bash

#set -x
# chkconfig 2345 on 
# description: HAProxy is a TCP/HTTP reverse proxy which is particularly suited for high availability environments.
if [ `whoami` = "root" ];then  
    echo "root用户！"  
else  
    echo "请使用root用户执行该命令，或者使用sudo！"  
    exit 1;
fi  

config="/usr/local/haproxy/conf/haproxy.cfg"
exec="/usr/local/haproxy/sbin/haproxy"
PID="/usr/local/haproxy/var/run/haproxy.pid"
if [ -f $config ];then
   echo ""
else
   echo "/usr/local/haproxy/conf/haproxy.cfg配置文件不存在，请检查"
   exit 1;
fi 

RETVAL=0 
start() { 
  $exec -c -q -f $config 
    if [ $? -ne 0 ]; then 
        echo "Errors found in configuration file." 
        return 1 
    fi 
  echo -n "Starting HAproxy: " 
  $exec -D -f $config -p $PID
  RETVAL=$? 
  echo 
  [ $RETVAL -eq 0 ]  
  return $RETVAL 
}

stop() { 
 echo -n "Shutting down HAproxy: " 
 kill `cat $PID`
 RETVAL=$? 
 echo 
 [ $RETVAL -eq 0 ] && rm -f $PID 
 return $RETVAL 
}

restart() { 
 $exec -c -q -f $config 
   if [ $? -ne 0 ]; then 
       echo "Errors found in configuration file, check it with 'haproxy check'." 
       return 1 
   fi 
 stop 
 start 
}

rhstatus() { 
 status haproxy 
}

check(){
 $exec -c -f $config
}


# See how we were called. 
case "$1" in 
 start) 
        start 
        ;; 
 stop) 
        stop 
        ;; 
 restart) 
        restart 
        ;; 
 status) 
        rhstatus 
        ;; 
 check)
        check
        ;;
 *) 
        echo $"Usage: haproxy {start|stop|restart|status|check}" 
        RETVAL=1 
esac 
exit $RETVAL 
