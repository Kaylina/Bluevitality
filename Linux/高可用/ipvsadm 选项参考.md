* Director Server:          提供"Load Balancer"功能的服务器
* virtual-service-address:  是指虚拟服务器的ip地址  
* real-service-address:     是指真实服务器的ip地址  
* scheduler:                调度方法


#### 格式
```
ipvsadm -A|E -t|u|f virutal-service-address:port [-s scheduler] [-p [timeout]] [-M netmask]
ipvsadm -D -t|u|f virtual-service-address
ipvsadm -C
ipvsadm -R
ipvsadm -S [-n]
ipvsadm -a|e -t|u|f service-address:port -r real-server-address:port [-g|i|m] [-w weight]
ipvsadm -d -t|u|f service-address -r server-address
ipvsadm -L|l [options]
ipvsadm -Z [-t|u|f service-address]
ipvsadm --set tcp tcpfin udp
ipvsadm --start-daemon state [--mcast-interface interface]
ipvsadm --stop-daemon
ipvsadm -h
```
#### 命令选项解释
```
-A --add-service 在内核的虚拟服务器表中添加一条新的虚拟服务器记录。也就是增加一台新的虚拟服务器。
-E --edit-service 编辑内核虚拟服务器表中的一条虚拟服务器记录 ( 修改LB算法：ipvsadm -E -t 172.16.1.253:80 -s wrr )
-D --delete-service 删除内核虚拟服务器表中的一条虚拟服务器记录 eg: ipvsadm -D -t 172.16.1.253:80
-C --clear 清除内核虚拟服务器表中的所有记录 
-R --restore 恢复虚拟服务器规则 eg: ipvsadm -S > /path/to/somefile
-S --save 保存虚拟服务器规则，输出为-R 选项可读的格式 eg: ipvsadm -R < /path/form/somefile
-a --add-server 在内核虚拟服务器表的一条记录里添加一条新的真实服务器记录。
-e --edit-server 编辑一条虚拟服务器记录中某条真实服务器记录 ( 修改RS权重：ipvsadm -e -t 1.1.1.1:80 -r 1.1.1.2 –g -w 3 )
-d --delete-server 删除一条虚拟服务器记录中的某条真实服务器记录 eg:  ipvsadm -d -t 172.16.1.253:80 -r 172.16.1.101
-L|-l --list 显示内核虚拟服务器表
-Z --zero 虚拟服务表计数器清零（清空当前的连接数量等）
--set tcp tcpfin udp 设置连接超时值
--start-daemon 启动同步守护进程。后面可以是master或backup，来说明其主备身份。也可用keepalived的VRRP功能
--stop-daemon 停止同步守护进程
-h --help 

其他选项:
-t --tcp-service service-address 说明虚拟服务器提供的是tcp服务 [vip:port] or [real-server-ip:port]
-u --udp-service service-address 说明虚拟服务器提供的是udp服务 [vip:port] or [real-server-ip:port]
-f --fwmark-service fwmark 说明是经过iptables 标记过的服务类型。
-s --scheduler scheduler 使用的调度算法：rr|wrr|lc|wlc|lblc|lblcr|dh|sh|sed|nq 默认是 wlc
-p --persistent [timeout] 持久稳固的服务。来自同1个客户的多次请求将被同一台RS处理。timeout 的默认值为300s
-M --netmask netmask persistent granularity mask
-r --real-server server-address 真实的服务器 [Real-Server:port]
-g --gatewaying 指定工作模式为DR模式（也是LVS 默认的模式）
-i --ipip 指定工作模式为隧道模式
-m --masquerading 指定工作模式为NAT模式
-w --weight weight 后端RS的权值
--mcast-interface interface 指定组播的同步接口
-c --connection 显示LVS 目前的连接 如：ipvsadm -L -c
--timeout 显示tcp tcpfin udp 的timeout 值 如：ipvsadm -L --timeout
--daemon 显示同步守护进程状态
--stats 显示统计信息
--rate 显示速率信息
--sort 对虚拟服务器和真实服务器排序输出
--numeric -n 输出IP 地址和端口的数字形式
```
