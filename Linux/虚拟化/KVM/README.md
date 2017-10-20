#### Install
```bash
#检测硬件是否支持虚拟化
#如果含有vmx或者svm字样则表示支持CPU虚拟化，Intel是vmx，AMD是svm
#也需要检测是否有kvm_xxx模块，如果装载不成功可能是没有开启硬件虚拟化,需要bios中开启
[root@wy ~]# egrep '(vmx|svm)' --color=always /proc/cpuinfo     
[root@wy ~]# modprobe kvm     
[root@wy ~]# modprobe kvm_intel || modprobe kvm_amd

#安装rpm包，并启动服务
[root@wy ~]# yum -y install kvm  python-virtinst libvirt tunctl bridge-utils virt-manager \
qemu-kvm-tools virt-viewer virt-v2v libguestfs-tools 
[root@wy ~]# systemctl start libvirtd

#检查是否有kvm模块,如果有则继续
[root@wy ~]# lsmod | grep kvm     
kvm_intel       52570  30      
kvm             314739 1 kvm_intel    
```

#### 配置桥接网络 br0
```bash
[root@wy ~]# cd /etc/sysconfig/network-scripts/
[root@wy ~]# cp ifcfg-eth0 ifcfg-br0

[root@wy ~]# vim ifcfg-eth0:     
DEVICE=eth0     
TYPE=Ethernet     
ONBOOT=yes     
NM_CONTROLLED=yes     
BRIDGE="br0"    <----
BOOTPROTO=static     
IPADDR="192.168.2.149"     
NETMASK="255.255.255.0"     
GATEWAY="192.168.2.2"     
 
[root@wy ~]# vim ifcfg-br0:
DEVICE=br0    <----
TYPE=Bridge     
ONBOOT=yes     
NM_CONTROLLED=yes     
BOOTPROTO=static     
IPADDR="192.168.2.149"     
NETMASK="255.255.255.0"     
GATEWAY="192.168.2.2"     

systemctl restart network
```
## 部署安装虚拟机
#### 建立磁盘文件
```bash
#如果使用的是raw格式就不需要了，kvm虚拟机默认使用raw格式的镜像格式，性能最好，速度最快
#它的缺点就是不支持一些新的功能，如支持快照镜像,zlib磁盘压缩,AES加密等。这里使用qcow2格式
[root@wy ~]# mkdir /opt/vms
[root@wy ~]# qemu-img create -f qcow2 /opt/vms/centos63-webtest.img 40G
```
####  建立虚拟机
下面展示多种方式建立虚拟机
```bash
########### 使用使用iso来安装 ###########     
[root@wy ~]# virt-install \     
--name=centos5 \     
--os-variant=RHEL5 \     
--ram=512 \     
--vcpus=1 \     
--disk path=/opt/vms/centos63-webtest.img,format=qcow2,size=7,bus=virtio \     
--accelerate \     
--cdrom /data/iso/CentOS5.iso \     
--vnc --vncport=5910 \     
--vnclisten=0.0.0.0 \     
--network bridge=br0,model=virtio \     
--noautoconsole

########### 使用使用nat模式网络###########     
[root@wy ~]# virt-install \     
--name=centos5 \     
--os-variant=RHEL5 \     
--ram=512 \     
--vcpus=1 \     
--disk path=/opt/vms/centos63-webtest.img,format=qcow2,size=7,bus=virtio \     
--accelerate \     
--cdrom /data/iso/CentOS5.iso \     
--vnc --vncport=5910 \     
--vnclisten=0.0.0.0 \     
--network network=default,model=virtio \     
--noautoconsole

########## 从http安装，使用ks, 双网卡, 启用console ########     
[root@wy ~]# virt-install \     
--name=centos63-webtest \     
--os-variant=RHEL6 \     
--ram=4096 \     
--vcpus=4 \     
--virt-type kvm  \     
--disk path=/opt/vms/centos63-webtest.img,format=qcow2,size=7,bus=virtio \     
--accelerate  \     
--location http://111.205.130.4/centos63 \     
--extra-args "linux ip=59.151.73.22 netmask=255.255.255.224 gateway=59.151.73.1 \ 
ks=http://111.205.130.4/ks/xen63.ks console=ttyS0  serial" \
--vnc --vncport=5910 --vnclisten=0.0.0.0 \     
--network bridge=br0,model=virtio \     
--network bridge=br1,model=virtio \     
--force \     
--noautoconsole

########## 安装windows ######## (不能使用virtio，因为默认windows没有virtio的硬盘和网卡驱动)
[root@wy ~]# virt-install \     
--name=win7-test \     
--os-variant=win7 \     
--ram=4096 \     
--vcpus=4 \      
--disk path=/opt/vms/centos63-webtest.img,size=100 \     
--accelerate  \     
--cdrom=/opt/iso/win7.iso       
--vnc --vncport=5910 --vnclisten=0.0.0.0 \     
--network bridge=br0 \       
--force \     
--noautoconsole

# 参数说明：     
# --name指定虚拟机名称     
# --ram分配内存大小。     
# --vcpus分配CPU核心数，最大与实体机CPU核心数相同     
# --disk指定虚拟机镜像，size指定分配大小单位为G。     
# --network网络类型，此处用的是默认，一般用的应该是bridge桥接。可以指定两次也就是两块网卡     
# --accelerate加速     
# --cdrom指定安装镜像iso     
# --location 从ftp,http,nfs启动     
# --vnc启用VNC远程管理     
# --vncport指定VNC监控端口，默认端口为5900，端口不能重复。     
# --vnclisten指定VNC绑定IP，默认绑定127.0.0.1，这里改为0.0.0.0。     
# --os-type=linux,windows     
# --extra-args指定额外的安装参数     
# --os-variant= [win7 vista winxp win2k8 rhel6 rhel5]     
# --force 如果有yes或者no的交互式，自动yes     
```
#### 安装系统
安装系统 有三种方式，通过VNC安装， 通过virt-manager安装 ， 通过console配合ks安装
```bash
#通过VNC来安装
#下载TightVNC连接上vnc安装，只需TightVNC Client即可。如果使用RealVNC就设置ColourLevel=rgb222才能连接
#端口号是安装时指定的，以后的安装流程和普通的是一样的

#通过virt-manager,
#如果你使用xshell那么可以不用安装x window就可以使用virt-manager, 需要安装 x11相关软件
[root@wy ~]# yum -y install libX11 xorg-x11-server-utils xorg-x11-proto-devel dbus-x11 \
xorg-x11-xauth xorg-x11-drv-ati-firmware  xorg-x11-xinit 
[root@wy ~]# virt-manager

#通过virt console
#如果安装时启用了 console可以使用 console来安装。Ctrl+] 可以退出console

#通过virt-viewer
[root@wy ~]# yum -y install virt-viewer xorg-x11-font* virt-viewer centos63-webtest 
```

## KVM管理
#### virsh 常见命令
```bash
1.virsh进入交互模式，在该交互模式下有命令补全。
   virsh # help list   #详细帮助     
2. virsh list --all #查看虚拟机状态     
3. virsh start instanceName #虚拟机开机     
4. virsh shutdown instanceName #虚拟机关机（需要Linux母体机电源管理 service acpid start）  
5. virsh destroy instanceName  #强制关机     
6. virsh create /etc/libvirt/qemu/wintest01.xml #通过以前的配置文件创建虚拟机     
7. virsh autostart instanceName #配置自启动     
8. virsh dumpxml wintest01 > /etc/libvirt/qemu/wintest02.xml #导出配置文件     
9. virsh undefine wintest01 #删除虚拟机配置文件，不会真的删除虚拟机     
10. mv /etc/libvirt/qemu/wintest02.xml /etc/libvirt/qemu/wintest01.xml ; \ 
    virsh define /etc/libvirt/qemu/wintest01.xml      #重新定义虚拟机
11. virsh edit wintest01  #编辑虚拟机配置文件     
12. virsh suspend wintest01  #挂起虚拟机     
13. virsh resume wintest01 #恢复挂起虚拟机     
```

#### 克隆
```bash
#一.使用virt-manager克隆，这个太简单就不演示了，需注意的是如果启用了VNC记得记得更改VNC的端口
#否则启动会失败的，见命令方式修改VNC修改

#二.使用命令克隆虚拟机
    Example：
    [root@wy ~]# virt-clone -o centos63_webtest -n centos63_webtest2 -f /opt/vms/centos_webtest2.img
    #参数说明:     
         -o –-original  #原来实例name     
         -n –-name      #新实例名称     
         -f –-file      #新实例磁盘存放位置
    #注：若启用了vnc则需修改配置文件的vnc端口否则启动失败，文件为：/etc/libvirt/qemu实例名.xml
        #或执行命令直接修改：
            [root@wy ~]# virsh edit <实例名>  ---->  <graphics type='vnc' port='5915'   ............
#三.启动克隆机
#有的Linux版本可能生成的网卡有问题，请修改 /etc/udev/rules.d/70-persistent-cd.rules 重启虚拟机)
[root@wy ~]# virsh start <实例名>
```
#### 快照
```bash
#kvm虚拟机默认使用raw格式的镜像格式，性能最好，速度最快
#它的缺点是不支持一些新功能，如支持镜像,zlib磁盘压缩,AES加密等。要使用镜像功能则磁盘格式必须为qcow2

#查看磁盘格式
[root@wy ~]# qemu-img info /opt/vms/centos63-119.22.img      
image: /opt/vms/centos63-119.22.img     
file format: qcow2     
virtual size: 40G (42949672960 bytes)     
disk size: 136K     
cluster_size: 65536 

#如果不是qcow2需要关机转换磁盘格式，如果是请跳过
[root@wy ~]# cp centos63-119.22.img centos63-119.22.raw     
[root@wy ~]# qemu-img convert -f raw -O qcow2 centos63-119.22.raw  centos63-119.22.img

启动vm, 建立快照，以后可以恢复 (快照配置文件在/var/lib/libvirt/qemu/snapshot/实例名/..)
[root@wy ~]# virsh start centos63-119.22     
[root@wy ~]# virsh snapshot-create centos63-119.22 

#恢复快照，可以建立一些测试文件，准备恢复
[root@wy ~]# ls /var/lib/libvirt/qemu/snapshot/centos63-119.22
1410341560.xml    
[root@wy ~]# virsh snapshot-revert centos63-119.22 1410341560

删除快照
[root@wy ~]# qemu-img info   centos63-119.22     
1         1410341560             228M 2014-04-08 10:26:40   00:21:38.053 
[root@wy ~]# virsh snapshot-delete centos63-119.2 1410341560
```

#### 添加网卡
```bash
#线上服务器是双网卡，一个走内网一个走外网。但初始虚拟机时没有指定两个网卡,这样需要添加网卡了
#比如已经将br1桥接到em2了，如果不会见刚开始br0桥接em1

#通过virt-manager来添加
#简单说一下：选中虚拟机 -- Open -- Details – AddHardware 选择网卡模式，mac不要重复，确定即可

#通过命令来添加
#1.使用virsh attach-interface 为虚拟机添加网卡
[root@wy ~]# virsh attach-interface centos63-119.23 --type bridge --source br1 --model virtio
#2.导入配置文件并覆盖原来的， 因为attach-interface添加后，只是在虚拟机中生效了，配置文件并没有改变
[root@wy ~]# cd /etc/libvirt/qemu
[root@wy ~]# virsh dumpxml centos63-119.23 > centos63-119.23.xml
#3.修改GuestOS中网卡配置文件，为另一个网卡配置IP
[root@wy ~]# cd /etc/sysconfig/network-scripts  
略
```
#### 硬盘扩容
```bash
#原来的/opt目录随着使用，空间渐渐满了，这时候我们就需要给/opt的挂载分区扩容了
#有两种情况 1. 该分区是lvm格式 2. 不是lvm格式，且不是扩展分区

#一. 分区是lvm格式 这种很简单，添加一块磁盘，lvm扩容
    #virt-manager添加方式和添加网卡一样，不再赘述，下面是使用命令来添加
    #1. 建立磁盘，并附加到虚拟机中
    [root@wy ~]# qemu-img create -f raw 10G.img 10G     
    [root@wy ~]# virsh attach-disk centos-1.2 /opt/kvm/5G.img vdb  
    #添加qcow2磁盘
    [root@wy ~]# qemu-img create -f qcow2 10G.img 10G     
    [root@wy ~]# virsh attach-disk centos-1.2 /opt/kvm/5G.img vdb --cache=none --subdriver=qcow2 
    #说明:       
    #centos-1.2       虚拟机的名称     
    #/opt/kvm/5G.img    附加的磁盘     
    #vdb                添加为哪个磁盘, 也就是在guestos中的名字
    #2. 导出并覆盖原来的配置文件，和网卡一样，attach后只是在虚拟机中生效
    [root@wy ~]# virsh dumpxml centos-1.2 > centos63-119.23.xml
    #3. 使用lvm在线扩容，详见 http://www.cnblogs.com/cmsd/p/3964118.html
    
#二. 分区不是lvm格式，该分区不是扩展分区, 需要关机离线扩展
    1.  新建一个磁盘，大于原来的容量，比如原来是40G，你想对某个分区扩容20G那么
    [root@wy ~]# qemu-img create -f qcow2 60G.img 60G
    2. 备份原来的磁盘，以防三长两短
    [root@wy ~]# cp centos63-119.27.img centos63-119.27.img.bak
    3. 查看原来的磁盘决定扩容哪一个分区
    [root@wy ~]# virt-filesystems --partitions --long -a centos63-119.27.img     
    [root@wy ~]# virt-df centos63-119.27.img 
    4. 扩容GuestOS的sda2
    [root@wy ~]# virt-resize --expand /dev/sda2 centos63-119.27.img 60G.img      
    #说明：  
    #/dev/sda2              扩容guestos的/dev/sda2     
    #centos63-119.27.img    原来的磁盘文件
    #60G                    第一步建立的更大的磁盘文件    
    5. 使用新磁盘启动
   [root@wy ~]# mv 60G.img centos63-119.27.img      
   [root@wy ~]# virsh start centos63-119.27
   #virt-resize其实就是将原来磁盘中的文件复制到新的文件中，将想要扩大的分区扩大了
```
#### 动态迁移
```
参考：
https://www.chenyudong.com/archives/virsh-kvm-live-migration-with-libvirt.html
```
