[root@localhost ~]# grep -v "^$" ip
192.168.1.5 
192.168.1.5 
192.168.1.13 
192.168.1.8 
192.168.1.15 
192.168.1.19 
[root@localhost ~]# < ip awk '!/^$/{ip_count[$1]++}END{for(i in ip_count){print ip_count[i]"\t"i}}' | sort -r  #统计IP出现次数
2       192.168.1.5
1       192.168.1.8
1       192.168.1.19
1       192.168.1.15
1       192.168.1.13

[root@localhost ~]# awk 'BEGIN{print ENVIRON["PATH"];}'
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin

[root@localhost ~]# awk 'BEGIN{OFMT="%.3f";print 2/3,123.11111111;}' /etc/passwd   
0.667 123.111
