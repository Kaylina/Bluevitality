#### 七种模式
```
Mode=0(balance-rr) 
表示负载分担round-robin，和交换机的聚合强制不协商的方式配合。

Mode=1(active-backup) 
表示主备模式，只有一块网卡是active,另外一块是备的，此时若交换机配的是捆绑将非正常工作，因交换机往两块网卡发包时有一半是丢弃的

Mode=2(balance-xor) 
表示XOR Hash负载分担，和交换机的聚合强制不协商方式配合。（需要xmit_hash_policy）

Mode=3(broadcast) 
表示所有包从所有interface发出，这个不均衡，只有冗余机制...和交换机的聚合强制不协商方式配合。

Mode=4(802.3ad) 
表示支持802.3ad协议，和交换机的聚合LACP方式配合（需要xmit_hash_policy）

Mode=5(balance-tlb) 
是根据每个slave的负载情况选择slave进行发送，接收时使用当前轮到的slave

Mode=6(balance-alb) 
在5的tlb基础上增加了rlb。

常用的有三种：
mode=0  平衡负载模式，有自动备援，但需要”Switch”支援及设定
mode=1  自动备援模式，其中一条线若断线，其他线路将会自动备援
mode=6  平衡负载模式，有自动备援，不必”Switch”支援及设定

需要说明的是如果想做成mode 0的负载均衡,仅仅设置这里options bond0 miimon=100 mode=0是不够的
与网卡相连的交换机必须做特殊配置（这两个端口应该采取聚合方式），因为做bonding的这两块网卡是使用同一个MAC地址
cisco称为 ethernetchannel
foundry称为 portgroup
```

#### 网口绑定
通过网口绑定(bond)技术,可以很容易实现网口冗余，负载均衡，从而达到高可用高可靠的目的。前提约定：  
* 2个物理网口分别是：  eth{0,1}  
* 绑定后的虚拟口是：   bond0  
```bash
[root@test ~]# cat /etc/sysconfig/network-scripts/ifcfg-bond0
DEVICE=bond0
BOOTPROTO=none
ONBOOT=yes
IPADDR=192.168.0.100
NETMASK=255.255.255.0
NETWORK=192.168.0.0
BROADCAST=192.168.0.255
DNS=192.168.10.1
NM_CONTROLLED=no
USERCTL=no

[root@test ~]# cat /etc/sysconfig/network-scripts/ifcfg-eth0
DEVICE=eth0
BOOTPROTO=none
MASTER=bond0
SLAVE=yes

[root@test ~]# cat /etc/sysconfig/network-scripts/ifcfg-eth1
DEVICE=eth1
BOOTPROTO=none
MASTER=bond0
SLAVE=yes

[root@test ~]# vim /etc/modprobe.d/bonding.conf
alias bond0 bonding
options bonding mode=0 miimon=100   #自动切换时间为100毫秒（在一般的实际应用中，0和1用的比较多）

[root@test ~]# modprobe bonding && lsmod | grep bonding
[root@test ~]# /etc/init.d/network restart
[root@test ~]# cat /proc/net/bonding/bond0
Ethernet Channel Bonding Driver: v3.5.0 (November 4, 2008)
Bonding Mode: fault-tolerance (active-backup)
Primary Slave: None
Currently Active Slave: eth0
......

[root@test ~]# ifconfig | grep HWaddr
bond0 Link encap:Ethernet HWaddr 00:16:36:1B:BB:74
eth0  Link encap:Ethernet HWaddr 00:16:36:1B:BB:74
eth1  Link encap:Ethernet HWaddr 00:16:36:1B:BB:74

#系统启动自动绑定、增加默认网关：
[root@test ~]# tail -2 /etc/rc.d/rc.local
ifenslave bond0 eth0 eth1
route add default gw 192.168.0.1
```
