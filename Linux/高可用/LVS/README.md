#### DR
```bash
yum install -y ipvsadm

# 前端 director 设置
echo 1 > /proc/sys/net/ipv4/ip_forward

ifconfig eth0:0 down
ifconfig eth0:0 192.168.0.38 broadcast 192.168.0.38 netmask 255.255.255.255 up
route add -host 192.168.0.38 dev eth0:0

ipvsadm -C
ipvsadm -A -t 192.168.0.38:80 -s wrr 
ipvsadm -a -t 192.168.0.38:80 -r 192.168.0.18:80 -g -w 3
ipvsadm -a -t 192.168.0.38:80 -r 192.168.0.28:80 -g -w 1

# 查看规则
ipvsadm -ln

# 后端 RS 设置
vip=192.168.0.38
ifconfig lo:0 $vip broadcast $vip netmask 255.255.255.255 up    #注意是在本地的loopbak
route add -host $vip lo:0
echo "1" >/proc/sys/net/ipv4/conf/lo/arp_ignore
echo "2" >/proc/sys/net/ipv4/conf/lo/arp_announce
echo "1" >/proc/sys/net/ipv4/conf/all/arp_ignore
echo "2" >/proc/sys/net/ipv4/conf/all/arp_announce

# 或用 RS 脚本：
SNS_VIP=192.168.0.38

case "$1" in 
start) 
      ifconfig lo:0 $SNS_VIP netmask 255.255.255.255 broadcast $SNS_VIP 
      /sbin/route add -host $SNS_VIP dev lo:0 
      echo "1" >/proc/sys/net/ipv4/conf/lo/arp_ignore 
      echo "2" >/proc/sys/net/ipv4/conf/lo/arp_announce 
      echo "1" >/proc/sys/net/ipv4/conf/all/arp_ignore 
      echo "2" >/proc/sys/net/ipv4/conf/all/arp_announce 
      sysctl -p >/dev/null 2>&1 
      echo "RealServer Start OK" 
      ;; 
stop) 
     ifconfig lo:0 down 
      route del $SNS_VIP >/dev/null 2>&1 
      echo "0" >/proc/sys/net/ipv4/conf/lo/arp_ignore 
      echo "0" >/proc/sys/net/ipv4/conf/lo/arp_announce 
      echo "0" >/proc/sys/net/ipv4/conf/all/arp_ignore 
      echo "0" >/proc/sys/net/ipv4/conf/all/arp_announce 
      echo "RealServer Stoped" 
      ;; 
*) 
      echo "Usage: $0 {start|stop}" 
      exit 1 
esac 

```
#### NAT
```bash
yum install -y ipvsadm

# 前端 director 设置
echo 1 > /proc/sys/net/ipv4/ip_forward
# 关闭 icmp 重定向
echo 0 > /proc/sys/net/ipv4/conf/all/send_redirects
echo 0 > /proc/sys/net/ipv4/conf/default/send_redirects
echo 0 > /proc/sys/net/ipv4/conf/eth0/send_redirects
echo 0 > /proc/sys/net/ipv4/conf/eth1/send_redirects
# 设置 nat
iptables -t nat -F
iptables -t nat -X
iptables -t nat -A POSTROUTING -s 192.168.0.0/24 -j MASQUERADE

ipvsadm -C
ipvsadm -A -t 172.16.254.200:80 -s wrr
ipvsadm -a -t 172.16.254.200:80 -r 192.168.0.18:80 -m -w 1
ipvsadm -a -t 172.16.254.200:80 -r 192.168.0.28:80 -m -w 1

# 查看规则
ipvsadm -ln

# 后端 RS 设置
在后端若干 RS 上设置其网关的 IP 为 director 的内网 IP 地址即可！
```
#### TUN
```bash

# 前端 DR 设置
echo 1 > /proc/sys/net/ipv4/ip_forward

/sbin/service network stop
ifconfig eno16777736:0 192.168.80.120 netmask 255.255.255.255 broadcast 192.168.80.120 up
/sbin/route add -host 192.168.80.120 dev eno16777736:0
/sbin/service network start

echo "0" > /proc/sys/net/ipv4/ip_forward
echo "1" > /proc/sys/net/ipv4/conf/all/send_redirects
echo "1" > /proc/sys/net/ipv4/conf/default/send_redirects
echo "1" > /proc/sys/net/ipv4/conf/eth0/send_redirects

ipvsadm -A -t 192.168.80.120:8080 -s rr
ipvsadm -a -t 192.168.80.120:8080 -r 192.168.80.135 -i
ipvsadm -a -t 192.168.80.120:8080 -r 192.168.80.136 -i


# 后端 RS 脚本

#!/bin/bash    
#description : start realserver  
VIP=192.168.80.120  
/etc/rc.d/init.d/functions  
case "$1" in  
start)  
echo " start LVS of REALServer"  
modprobe ipip  #加载好ipip模块后会有默认的tunl0隧道
echo "0" > /proc/sys/net/ipv4/ip_forward
/sbin/ifconfig tunl0 $VIP netmask 255.255.255.255 broadcast $VIP  
echo "1" > /proc/sys/net/ipv4/conf/tunl0/arp_ignore  
echo "2" > /proc/sys/net/ipv4/conf/tunl0/arp_announce  
echo "1" > /proc/sys/net/ipv4/conf/all/arp_ignore  
echo "2" > /proc/sys/net/ipv4/conf/all/arp_announce  
echo "0" > /proc/sys/net/ipv4/conf/tunl0/rp_filter
echo "0" > /proc/sys/net/ipv4/conf/all/rp_filter
# tunl0/rp_filter 默认为1 ，需要改为0，关闭此功能。
#Linux的rp_filter用于实现反向过滤技术，也即uRPF，它验证反向数据包的流向，以避免伪装IP攻击 。 
#然而，在LVS TUN 中，数据包是有问题的，因为从realserver eth0 出去的包源IP应为192.168.1.62，而不是VIP。
#所以必须关闭返一项功能。 
#DR和TUN在网络层实际上使用了一个伪装IP数据包的功能。让client收到数据包后，迒回的请求再次转给分发器。
#
;;  
stop)  
/sbin/ifconfig tunl0 down  
echo "close LVS Directorserver"  
echo "0" > /proc/sys/net/ipv4/conf/tunl0/arp_ignore  
echo "0" > /proc/sys/net/ipv4/conf/tunl0/arp_announce  
echo "0" > /proc/sys/net/ipv4/conf/all/arp_ignore  
echo "0" > /proc/sys/net/ipv4/conf/all/arp_announce  
echo "1" > /proc/sys/net/ipv4/conf/tunl0/rp_filter  
echo "1" > /proc/sys/net/ipv4/conf/all/rp_filter  
;;  
*)  
echo "Usage: $0 {start|stop}"  
exit 1  
esac 
```
