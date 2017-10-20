#!/bin/bash
#this is a server firewall 

#define variable PATH

IPT=/sbin/iptables

#Remove any existing rules
$IPT -F
$IPT -X
$IPT -Z

#setting default firewall policy
$IPT --policy OUTPUT ACCEPT
$IPT --policy FORWARD DROP
$IPT -P INPUT DROP

#setting for loopback interface
$IPT -A INPUT -i lo -j ACCEPT
$IPT -A OUTPUT -o lo -j ACCEPT

# Source Address Spoofing and Other Bad Addresses
#$IPT -A INPUT -i eth0 -s 172.16.0.0/12 -j DROP
#$IPT -A INPUT -i eth0 -s 0.0.0.0/8 -j DROP
#$IPT -A INPUT -i eth0 -s 169.254.0.0/16 -j DROP
#$IPT -A INPUT -i eth0 -s 192.0.2.0/24 -j DROP

# prevent all Stealth Scans and TCP State Flags
$IPT -A INPUT -p tcp --tcp-flags ALL ALL -j DROP
# All of the bits are cleared
$IPT -A INPUT -p tcp --tcp-flags ALL NONE -j DROP
$IPT -A INPUT -p tcp --tcp-flags ALL FIN,URG,PSH -j DROP
#SYN and RST are both set
$IPT -A INPUT -p tcp --tcp-flags SYN,RST SYN,RST -j DROP
# SYN and FIN are both set
$IPT -A INPUT -p tcp --tcp-flags SYN,FIN SYN,FIN -j DROP
# FIN and RST are both set
$IPT -A INPUT -p tcp --tcp-flags FIN,RST FIN,RST -j DROP
# FIN is the only bit set, without the expected accompanying ACK
$IPT -A INPUT -p tcp --tcp-flags ACK,FIN FIN -j DROP
# PSH is the only bit set, without the expected accompanying ACK
$IPT -A INPUT -p tcp --tcp-flags ACK,PSH PSH -j DROP
# URG is the only bit set, without the expected accompanying ACK
$IPT -A INPUT -p tcp --tcp-flags ACK,URG URG -j DROP



#setting access rules
#one,ip access rules,allow all the ips of 
$IPT -A INPUT -s 202.81.17.0/24 -p all -j ACCEPT
$IPT -A INPUT -s 202.81.18.0/24 -p all -j ACCEPT
$IPT -A INPUT -s 124.43.62.96/27 -p all -j ACCEPT
$IPT -A INPUT -s 192.168.1.0/24 -p all -j ACCEPT
$IPT -A INPUT -s 10.0.0.0/24 -p all -j ACCEPT
################################################

#second,port access rules
#nagios
$IPT -A INPUT  -s 192.168.1.0/24  -p tcp  --dport 5666 -j ACCEPT
$IPT -A INPUT  -s 202.81.17.0/24  -p tcp  --dport 5666 -j ACCEPT
$IPT -A INPUT  -s 202.81.18.0/24  -p tcp  --dport 5666 -j ACCEPT

#db
$IPT -A INPUT  -s 192.168.1.0/24  -p tcp  --dport 3306 -j ACCEPT
$IPT -A INPUT  -s 192.168.1.0/24  -p tcp  --dport 3307 -j ACCEPT
$IPT -A INPUT  -s 192.168.1.0/24  -p tcp  --dport 3308 -j ACCEPT
$IPT -A INPUT  -s 192.168.1.0/24  -p tcp  --dport 1521 -j ACCEPT

#ssh difference from other servers here.>>
$IPT -A INPUT -s 202.81.17.0/24  -p tcp  --dport 52113 -j ACCEPT
$IPT -A INPUT -s 202.81.18.0/24  -p tcp  --dport 52113 -j ACCEPT
$IPT -A INPUT -s 124.43.62.96/27  -p tcp  --dport 52113 -j ACCEPT
$IPT -A INPUT -s 192.168.1.0/24  -p tcp  --dport 52113 -j ACCEPT
#$IPT -A INPUT   -p tcp  --dport 22 -j ACCEPT
#ftp
#$IPT -A INPUT   -p tcp  --dport 21 -j ACCEPT

#http
$IPT -A INPUT   -p tcp  --dport 80 -j ACCEPT
$IPT -A INPUT   -s 192.168.1.0/24  -p tcp  -m multiport --dport 8080,8081,8082,8888,8010,8020,8030,8150 -j ACCEPT
$IPT -A INPUT   -s 202.81.17.0/24  -p tcp  -m multiport --dport 8080,8081,8082,8888,8010,8020,8030,8150 -j ACCEPT
$IPT -A INPUT   -s 124.43.62.96/27 -p tcp  -m multiport --dport 8080,8081,8082,8888,8010,8020,8030,8150 -j ACCEPT

#snmp
$IPT -A INPUT -s 192.168.1.0/24 -p UDP  --dport 161 -j ACCEPT 
$IPT -A INPUT -s 202.81.17.0/24 -p UDP  --dport 161 -j ACCEPT 
$IPT -A INPUT -s 202.81.18.0/24 -p UDP  --dport 161 -j ACCEPT 

#rsync
$IPT -A INPUT -s 192.168.1.0/24 -p tcp -m tcp --dport 873   -j ACCEPT
$IPT -A INPUT -s 202.81.17.0/24 -p tcp -m tcp --dport 873   -j ACCEPT
$IPT -A INPUT -s 202.81.18.0/24 -p tcp -m tcp --dport 873   -j ACCEPT
$IPT -A INPUT -s 124.43.62.96/27 -p tcp -m tcp --dport 873   -j ACCEPT

#nfs 2049,portmap 111
$IPT -A INPUT -s 192.168.1.0/24 -p udp  -m multiport --dport 111,892,2049 -j ACCEPT 
$IPT -A INPUT -s 192.168.1.0/24 -p tcp  -m multiport --dport 111,892,2049 -j ACCEPT 

#icmp
#$IPT -A INPUT -p icmp -m icmp --icmp-type any -j ACCEPT
$IPT -A INPUT -s 124.43.62.96/27 -p icmp -m icmp --icmp-type any -j ACCEPT
$IPT -A INPUT -s 192.168.1.0/24 -p icmp -m icmp --icmp-type any -j ACCEPT
#others RELATED
$IPT -A INPUT  -m state --state ESTABLISHED,RELATED -j ACCEPT
$IPT -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
