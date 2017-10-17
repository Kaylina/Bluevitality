#!/bin/bash

. /etc/rc.d/init.d/functions

VIP=192.168.0.30
RIP1=192.168.0.21
RIP2=192.168.0.22
PORT=80

case "$1" in
start)           

  /sbin/ifconfig eth0:3 $VIP broadcast $VIP netmask 255.255.255.255 up
  /sbin/route add -host $VIP dev eth0:3

  echo 1 > /proc/sys/net/ipv4/ip_forward

  /sbin/iptables -F
  /sbin/iptables -Z
  /sbin/ipvsadm -C

  /sbin/ipvsadm -A -t $VIP:80 -s wlc
  /sbin/ipvsadm -a -t $VIP:80 -r $RIP1 -g -w 1
  /sbin/ipvsadm -a -t $VIP:80 -r $RIP2 -g -w 2
  /bin/touch /var/lock/subsys/ipvsadm &> /dev/null
;; 

stop)

  echo 0 > /proc/sys/net/ipv4/ip_forward
  /sbin/ipvsadm -C
  /sbin/ifconfig eth0:3 down
  /sbin/route del $VIP
  
  /bin/rm -f /var/lock/subsys/ipvsadm
  
  echo "ipvs is stopped..."
;;

status)
  if [ ! -e /var/lock/subsys/ipvsadm ]; then
    echo "ipvsadm is stopped ..."
  else
    echo "ipvs is running ..."
    ipvsadm -L -n
  fi
;;
*)
  echo "Usage: $0 {start|stop|status}"
;;
esac
