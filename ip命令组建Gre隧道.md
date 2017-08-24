#### 环境
host A : `121.207.22.123`  
host B : `111.2.33.28`

#### HostA
> 创建一个GRE类型隧道设备gre1, 并设置对端IP为111.2.33.28。  
> 隧道数据包将被从121.207.22.123也就是本地IP地址发起，其TTL字段被设置为255。  
> 隧道设备分配的IP地址为10.10.10.1，掩码为255.255.255.0。  
```Bash
ip tunnel add GRE1 mode gre remote 111.2.33.28 local 121.207.22.123 ttl 255
ip link set GRE1 up
ip address add 10.10.10.1 peer 10.10.10.2 dev GRE1
sysctl -w net.ipv4.ip_forward=1
sysctl -p
```

#### HostB
```Bash
ip tunnel add GRE1 mode gre remote 121.207.22.123 local 111.2.33.28 ttl 255
ip link set GRE1 up
ip addr add 10.10.10.2 peer 10.10.10.1 dev GRE1
sysctl -w net.ipv4.ip_forward=1
sysctl -p
```

#### 检测连通性
```Bash
[root@wy ~]#ping 10.10.10.2 (host A)
PING 10.10.10.2 (10.10.10.2) 56(84) bytes of data.
64 bytes from 10.10.10.2: icmp_req=1 ttl=64 time=0.319 ms
64 bytes from 10.10.10.2: icmp_req=2 ttl=64 time=0.296 ms
64 bytes from 10.10.10.2: icmp_req=3 ttl=64 time=0.287 ms
```

#### 撤销隧道
```Bash
ip link set gre1 down
ip tunnel del gre1
```
  

## 附：
#### 环境
                                                  |
            1.1.1.1               2.2.2.2         |
            +---------+  Public   +---------+     | Private
            | ServerA +-----------+ ServerB +-----+
            +---------+  Network  +---------+     | Network
                                                  |
                                                  | 192.168.1.0/24 


#### ServerA
```Bash
ip tunnel add a2b mode ipip remote 2.2.2.2 local 1.1.1.1
ifconfig a2b 192.168.2.1 netmask 255.255.255.0
/sbin/route add -net 192.168.1.0/24 gw 192.168.2.2
```
#### ServerB
```Bash
ip tunnel add a2b mode ipip remote 1.1.1.1 local 2.2.2.2
ifconfig a2b 192.168.2.2 netmask 255.255.255.0
iptables -t nat -A POSTROUTING -s 192.168.2.1 -d 192.168.1.0/24 -j MASQUERADE
sysctl -w net.ipv4.ip_forward=1
sed -i '/net.ipv4.ip_forward/ s/0/1/'  /etc/sysctl.conf
```
至此，完成了两端的配置，ServerA可直接访问ServerB所接的私网了
