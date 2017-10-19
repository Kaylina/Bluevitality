
#### 备忘
GlusterFS 具有高扩展、高可性、高性能、可横向扩展等特点  
全局命名空间、分布式前端的高性能文件系统，没有元数据服务器的设计，使其没有单点故障问题  
集群中每个成员关系对等  

#### Install
```bash
#主机解析
tail -4 /etc/hosts
192.168.1.100 gfs-server1
192.168.1.107 gfs-server2
192.168.1.126 gfs-server3
192.168.1.217 gfs-server4

systemctl disable firewalld
systemctl stop firewalld
setenforce 0
echo "setenforce 0" >> /etc/rc.local

yum update  -y
yum install -y centos-release-gluster
yum install -y flex bison openssl openssl-devel libxml2-devel gcc rpcbind libaio lvm2-devel fuse-libs
yum install -y glusterfs glusterfs-fuse glusterfs-cli glusterfs-server glusterfs-api fuse
yum install -y ntp

#时间同步
crontab -l
0 23 * * * root  /usr/sbin/ntpdate time.windows.com &> /dev/null; /usr/sbin/clock -w

#启动服务
systemctl enable glusterd
systemctl start glusterd

#组建集群
for gfs_host in gfs-server{1..4}
do 
  gluster peer probe $gfs_host
done

#对每个集群成员进行分区格式化
parted /dev/sda mklabel gpt
parted /dev/sda mkpart logical ext3 20GB
partprobe
mkfs.xfs /dev/sda

# 创建磁盘挂载目录
mkdir -p /data/gfs
mount -t xfs /dev/sda /data/gfs
mkdir -p /data/gfs/brick0       #创建GlusterFS卷目录

#写入/etc/fstab.conf
echo "/dev/sdb /data/gfs xfs defaults 1 1" >> /etc/fstab
```
#### 分布式 Hash 卷
```bash
gluster volume create gfs_disk gfs-server{1..4}:/data/gfs/brick0
#默认情况下使用的就是分布式卷，以每个文件为对象分别写入各存储服务器
#当向 GlusterFS 写入文件时，GlusterFS 通过弹性 Hash 算法对文件名进行计算
#然后将其均匀的分布到各个节点上， 因此分布式 Hash 卷没有数据冗余 
```
#### 复制卷
```bash
gluster volume create gfs_disk replica 4 transport tcp gfs-server{1..4}:/data/gfs/brick0
#相当于 RAID1。向 GlusterFS 中存储文件时，GlusterFS 将其拷贝到所有节点，并且是同步的
#这会极大降低磁盘性能，并呈线性降低，但复制卷随着节点数量增加，起数据冗余能力也在增加

#Other Example：
gluster volume create <卷名> replica 2 192.168.10.{2,3}:/brick01/b1   192.168.10.{2,3}:/brick01/b2
#副本数需等于brick数，当brick数是副本倍数时则为Replicated-Distributed
#每2个brick成一组，每组2个副本，文件又以DHT分布在三个组上，是副本卷与分布式卷的组合
```
#### 分布式 Hash 复制卷
```bash
gluster volume create gfs_disk replica 2 transport tcp gfs-server{1..4}:/data/gfs/brick0 
#将 Hash 卷与复制卷整合一下，通过 replica 参数指定复制份数
#以上例子为使用4个节点创建，每两个节点组成一个复制卷，然后两对节点再组成 Hash 卷
```
#### 条带卷 Stripe
```bash
gluster volume create gfs_disk stripe 4 gfs-server{1..4}:/data/gfs/brick0
#类似RAID0，将数据条带化分布在不同brick，该方式将文件分成stripe块分别进行存储，在大文件读取时有优势
```

#### Replicated-Stripe-Distributed
```bash
#Other Example：
gluster volume create gfs_disk stripe 2 \
replica 2 192.168.2.{100,101,102}:/mnt/sdb1 192.168.2.{100,101,102}:/mnt/sdc1 192.168.2.{100,101}:/mnt/sdd1
#使用8个brick创建一个组合卷，即brick数是stripe*replica的倍数，则创建三种基本卷的组合卷
#若刚好等于stripe*replica则为stripe-Distrbuted卷
```

#### 客户端
```bash
mount -t glusterfs gfs-server1:gfs_disk /mnt/gfs
echo "gfs-server1:gfs_disk /mnt/gfs glusterfs defaults 0 1" >> /etc/fstab
```

#### 管理
```bash
#增加节点：
gluster peer probe 192.168.10.2

#删除节点使用：
gluster peer detach ......

#查看节点：
gluster peer status       #若每个节点都能看到其他节点则完成配置（仅在其中一个节点进行添加操作即可）
    Number of Peers: 2
    Hostname: server1
    Uuid: 5e987bda-16dd-43c2-835b-08b7d55e94e5
    State: Peer in Cluster (Connected)
    Hostname: server2
    Uuid: 1e0ca3aa-9ef7-4f66-8f15-cbc348f29ff7
    State: Peer in Cluster (Connected)

#启停卷：
gluster volume <start|stop> <卷名>

#查看卷：（存储池中的当前卷的信息，包括卷方式、包涵的brick、卷的当前状态、卷名及UUID等）
gluster volume info [卷名]

#卷状态：（当前卷状态，包括其中各brick状态，NFS状态及当前task执行情况，一些系统设置状态等）
gluster volume status            

#删除卷：     
gluster volume stop <卷名> ; gluster volume delete <卷名>

#卷同步：（当特定节点的卷信息丢失/删除时执行可使用其恢复回来）
gluster volume sync <ip> < all、卷名 >

#卷设置：

#访问地址授权： 
gluster volume set [卷名] auth.allow <192.168.10.*>

#拒绝访问授权： 
gluster volume set [卷名] auth.reject <192.168.10.*> #（需与allow配合使用）

#剩余容量阈值： 
gluster volume set cluster.min-free-disk <num>%

#磁盘条带大小： 
gluster volume set cluster.stripe-block-size <num>KB

#I/O线程数量：  
gluster volume set performance.io-thread-count 32    #默认16

#读缓存大小：   
gluster volume set performance.cache-size 64MB       #默认32

#关闭自带NFS：  
gluster volume set nfs.disabled on

#容量负载均衡：
gluster volume rebalance <卷名> start               #开始均衡

#增删BRICK后建议使用。当对卷进行了扩展或收缩后需对卷的数据重新均衡
gluster volume rebalance <卷名> status              #查看状态

#触发副本自愈：      gluster volume heal <卷名> info healed|heal-failed|split-brain 
    只修复有问题的文件：     gluster volume heal <卷名>
    修复所有文件：     gluster volume heal <卷名> full
    查看自愈详情：     gluster volume heal <卷名> info 

#替换Brick:
#执行replcace-brick卷替换启动，使用start启动命令后，开始将原始Brick的数据迁移到即将需要替换的Brick上
gluster volume replace-brick dht_vol server0:/mnt/sdb1 server0:/mnt/sdc1 start
#在迁移过程中，可查看替换任务是否完成
gluster volume replace-brick dht_vol server0:/mnt/sdb1 server0:/mnt/sdc1 status
#在迁移过程中，可以执行abort命令终止Brick替换
gluster volume replace-brick dht_vol server0:/mnt/sdb1 server0:/mnt/sdc1 abort
#在迁移结束后，执行commit结束任务则进行Brick替换。使用volume info命令可查看到Brick已经被替换
gluster volume replace-brick dht_vol server0:/mnt/sdb1 server0:/mnt/sdc1 commit

#brick管理：（在任意节点）
#增加BRICK：（容量将自动增加。若是副本卷则一次添加的Bricks数是replica的整数倍，stripe具有同样的要求）
gluster volume add-brick <卷名> <ip>:/brick01/b1    
#删除BRICK：（若是副本卷，则移除的Bricks数是replica的整数倍，stripe具有同样的要求）
#执行移除Brick时会将数据迁移到其他可用Brick，当结束后才将Brick移除。
#执行start命令开始迁移数据，正常移除Brick ，在执行开始后可使用status命令进行task状态查看。
gluster volume remove-brick <卷名> <ip>:/brick01/b1    [start/status/commit]             
#注：
#使用commit执行Brick移除则不会进行数据迁移而直接删除Brick，符合不需数据迁移的用户需求
#PS：系统的扩容及缩容可通过如上节点管理、Brick管理组合达到目的。
#(1)扩容时，可以先增加系统节点，然后添加新增节点上的Brick即可。
#(2)缩容时，先移除Brick，然后再进行节点删除则达到缩容的目的，且可以保证数据不丢失。

#Top监控： 所有的查看都可设置top数，默认100
#Top command允许查看bricks的性能
#如：read, write, file open calls, file read calls, file write calls \
#directory open calls, and directory real calls
#查看打开的fd ：     
gluster volume top VOLNAME open [brick BRICK-NAME] [list-cnt cnt]
#查看调用次数最多的读调用：
gluster volume top VOLNAME read [brick BRICK-NAME] [list-cnt cnt]
#查看调用次数最多的写调用：
gluster volume top VOLNAME write [brick BRICK-NAME] [list-cnt cnt]
gluster volume top VOLNAME opendir [brick BRICK-NAME] [list-cnt cnt]
gluster volume top VOLNAME readdir [brick BRICK-NAME] [list-cnt cnt]

#NFS方式： 
#Gluster提供内置的NFS服务，支持其他实现了NFSv3的客户端直接访问
#关闭Linux内核自带的NFS服务并启动rpc端口映射管理：
service nfs stop       
service rpcbind start
mount -t nfs -o vers=3 host/ip:/path mnt-port 

#GlusterFS的访问接口：
#类似于在VFS的下层的Filesystem驱动（FUSE常用）
#Files:    FUSE、SMB、NFS、Hadoop
#Blocks：     Qemu、Cinder
#Transports：     IP、RDMA
#Objects：     Swift(UFO)
#Whatever：     libgfapi
#Back ends：     files、BD、DB
```

#### 流程
```
applications ---> VFS ---> /dev/fuse ---> GlusterFS ~~~~TCP/IP或RDMA~~~~ GlusterFS ---> [ext3/xfs/...]
1. 在C端；用户通过glusterfs的mount point读写数据，对用户来说集群系统的存在对其完全透明
2. 用户的这个操作被递交给本地OS的VFS处理
3. VFS将数据递交给FUSE内核文件系统： 在启动glusterfs客户端前需向OS注册实际的文件系统：FUSE
4. ext4是对实际的磁盘进行处理而fuse则是将数据通过"/dev/fuse"设备文件递交给glusterfs client端。
注：可将fuse文件系统理解为代理

GlusterFS的卷类型：

一.基本卷：
    哈希卷：Distributed Volume  
    文件通过HASH算法在所有Brick上分布，文件级别RAID-0（不具有容错能力）
    
    复制卷：Replicated Volume           
    文件同步复制到多个Brick上，文件级别RAID-1（写性能下降，读性能提高，有容错能力） 生产环境推荐
    
    条带卷：Striped Volume          
    单个文件分布到多个Brick中从而支持超大文件，类似RAID-0，以Round-Robin方式（轮询）
    常用于HPC中超大文件的高并发访问

二.复合卷：哈希+复制（同时具有哈希卷和复制卷的特点）
    哈希复制卷：     ........
    哈希条带卷：     ........
    复制条带卷：     ........
    哈希复制条带卷：     ........
```

