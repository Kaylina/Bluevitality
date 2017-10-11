## 格式化
#### 例一
有多个块设备时可直接指定多个块设备进行格式化。并且可为metadata和data指定不同的profile级别  
[root@digoal ~]# `mkfs.btrfs -m raid10 -d raid10 -n 4096 -f /dev/sd{b..e}`  
```
btrfs-progs v4.3.1    
    
Label:              (null)  
UUID:               00036b8e-7914-41a9-831a-d35c97202eeb  
Node size:          4096  
Sector size:        4096  
Filesystem size:    80.00GiB  
Block group profiles:   
Data:             RAID10            2.01GiB  
Metadata:         RAID10            2.01GiB  
System:           RAID10           20.00MiB  
SSD detected:       no  
Incompat features:  extref, skinny-metadata  
Number of devices:  4  
Devices:  
ID        SIZE      PATH  
1         20.00GiB  /dev/sdb  
2         20.00GiB  /dev/sdc  
3         20.00GiB  /dev/sdd  
4         20.00GiB  /dev/sde 
  ```
#### 例二
metadata使用raid1(不使用条带)。而data使用raid10(使用条带)。可以看到system和metadata一样使用了raid1!...  
不过建议将metadata和data设置为一致的风格  
[root@digoal ~]# `mkfs.btrfs -m raid1 -d raid10 -n 4096 -f /dev/sd{b..e}`  
```
btrfs-progs v4.3.1  
   
Label:              (null)  
UUID:               4eef7b0c-73a3-430c-bb61-028b37d1872b  
Node size:          4096  
Sector size:        4096  
Filesystem size:    80.00GiB  
Block group profiles:  
Data:             RAID10            2.01GiB  
Metadata:         RAID1             1.01GiB  
System:           RAID1            12.00MiB  
SSD detected:       no  
Incompat features:  extref, skinny-metadata   
Number of devices:  4  
Devices:  
ID        SIZE      PATH  
1         20.00GiB  /dev/sdb  
2         20.00GiB  /dev/sdc  
3         20.00GiB  /dev/sdd  
4         20.00GiB  /dev/sde  
```
[root@digoal ~]#`btrfs filesystem show /dev/sdb`
```
Label: none  uuid: 4eef7b0c-73a3-430c-bb61-028b37d1872b
  Total   devices 4 FS bytes used 28.00KiB
  devid    1 size 20.00GiB used 2.00GiB path /dev/sdb
  devid    2 size 20.00GiB used 2.00GiB path /dev/sdc
  devid    3 size 20.00GiB used 1.01GiB path /dev/sdd
  devid    4 size 20.00GiB used 1.01GiB path /dev/sde
```

## 挂载
若btrfs管理了多个块设备，那么有两种方式挂载：
* 第一种是直接指定多个块设备
* 第二种是先scan再mount，因为某些系统重启或btrfs模块重加载后需重新scan来识别

#### 例如
[root@digoal ~]# `btrfs device scan`  
```
Scanning for Btrfs filesystems
```
[root@digoal ~]# `mount /dev/sdb /data01`  
[root@digoal ~]# `btrfs filesystem show /data01`  
```
Label: none  uuid: 00036b8e-7914-41a9-831a-d35c97202eeb
  Total devices 4 FS bytes used 1.03MiB
  devid    1 size 20.00GiB used 2.01GiB path /dev/sdb
  devid    2 size 20.00GiB used 2.01GiB path /dev/sdc
  devid    3 size 20.00GiB used 2.01GiB path /dev/sdd
  devid    4 size 20.00GiB used 2.01GiB path /dev/sde
```
#### 或者
[root@digoal ~]# `mount -o device=/dev/sdb,device=/dev/sdc,device=/dev/sdd,device=/dev/sde /dev/sdb /data01`  
[root@digoal ~]# `btrfs filesystem show /data01`  
```
Label: none  uuid: 00036b8e-7914-41a9-831a-d35c97202eeb
  Total devices 4 FS bytes used 1.03MiB
  devid    1 size 20.00GiB used 2.01GiB path /dev/sdb
  devid    2 size 20.00GiB used 2.01GiB path /dev/sdc
  devid    3 size 20.00GiB used 2.01GiB path /dev/sdd
  devid    4 size 20.00GiB used 2.01GiB path /dev/sde
```
#### 或者
[root@digoal ~]#`vi /etc/fstab`    
`UUID=00036b8e-7914-41a9-831a-d35c97202eeb /data01 btrfs ssd,ssd_spread,space_cache,recovery,defaults 0 0`  

## resize btrfs
> btrfs整合了块设备管理，其存储了data, metadata, system三种数据类型  
> 当任一类型需要空间时，btrfs会为其分配空间 (block group) ，这些分配的空间来自btrfs管理的块设备
> resize btrfs实际上就是resize块设备的使用空间
> 对于单个块设备的btrfs，resize btrfs root挂载点和resize block dev的效果是一样的

扩大文件系统容量。单位支持k,m,g
* btrfs filesystem resize 'amount' /mount-point
* btrfs filesystem show /mount-point
* btrfs filesystem resize devid:'amount' /mount-point
* btrfs filesystem resize devid:max /mount-point

缩小文件系统容量。单位支持k,m,g
* btrfs filesystem resize 'amount' /mount-point
* btrfs filesystem resize devid:'amount' /mount-point
* btrfs filesystem show /mount-point

#### example
对于单个块设备的btrfs则不需要指定块设备ID  
[root@digoal ~]# `btrfs filesystem resize +200M /btrfssingle`
```
Resize '/btrfssingle' of '+200M'
```
对于多个块设备的btrfs，需要指定块设备ID   
[root@digoal ~]# `btrfs filesystem show /data01`
```
Label: none  uuid: 00036b8e-7914-41a9-831a-d35c97202eeb
  Total devices 4 FS bytes used 2.12GiB
  devid    1 size 19.00GiB used 4.01GiB path /dev/sdb
  devid    2 size 20.00GiB used 4.01GiB path /dev/sdc
  devid    3 size 20.00GiB used 4.01GiB path /dev/sdd
  devid    4 size 20.00GiB used 4.01GiB path /dev/sde
```	
[root@digoal ~]# `btrfs filesystem resize '1:+1G' /data01`
```
Resize '/data01' of '1:+1G'
```
[root@digoal ~]# `btrfs filesystem show /data01`
```
Label: none  uuid: 00036b8e-7914-41a9-831a-d35c97202eeb
  Total devices 4 FS bytes used 2.12GiB
  devid    1 size 20.00GiB used 4.01GiB path /dev/sdb
  devid    2 size 20.00GiB used 4.01GiB path /dev/sdc
  devid    3 size 20.00GiB used 4.01GiB path /dev/sdd
  devid    4 size 20.00GiB used 4.01GiB path /dev/sde
```

可以指定max，表示使用块设备的所有容量   
[root@digoal ~]#`btrfs filesystem resize '1:max' /data01`
```
Resize '/data01' of '1:max'
```
减去特定大小容量  
[root@digoal ~]#`btrfs filesystem resize -200M /btrfssingle`
```
Resize '/btrfssingle' of '-200M'
```
指定其固定大小  
[root@digoal ~]# `btrfs filesystem resize 700M /btrfssingle`
```
Resize '/btrfssingle' of '700M'
```
同样支持max  
[root@digoal ~]# `btrfs filesystem resize 'max' /data01`
```
Resize '/data01' of 'max'
```
[root@digoal ~]# `btrfs filesystem resize '2:max' /data01`
```
Resize '/data01' of '2:max'
```
[root@digoal ~]# `btrfs filesystem resize '3:max' /data01`
```
Resize '/data01' of '3:max'
```
[root@digoal ~]# `btrfs filesystem resize '4:max' /data01`
```
Resize '/data01' of '4:max'
```
## 转换
若一开始btrfs只用了一个块设备，现要转换成raid1，如何转换?   
[root@digoal ~]# `mkfs.btrfs -m single -d single -n 4096 -f /dev/sdb`
```
btrfs-progs v4.3.1
See http://btrfs.wiki.kernel.org for more information.
Label:              (null)
UUID:               165f59f6-77b5-4421-b3d8-90884d3c0b40
Node size:          4096
Sector size:        4096
Filesystem size:    20.00GiB
Block group profiles:
  Data:             single            8.00MiB
  Metadata:         single            8.00MiB
  System:           single            4.00MiB
SSD detected:       no
Incompat features:  extref, skinny-metadata
Number of devices:  1
Devices:
   ID        SIZE       PATH
    1        20.00GiB   /dev/sdb
```
[root@digoal ~]#`mount -o ssd,ssd_spread,discard,noatime,compress=no,space_cache,defaults /dev/sdb /data01`  
[root@digoal ~]#`btrfs device add /dev/sdc /data01 -f`   
使用balance在线转换，其中-m指metadata, -d指data     
[root@digoal ~]#`btrfs balance start -dconvert=raid1 -mconvert=raid1 /data01`  
```
Done, had to relocate 3 out of 3 chunks
```
这里的chunks指的就是block group.   

[root@digoal ~]# `btrfs filesystem show /data01`
```
Label: none  uuid: 165f59f6-77b5-4421-b3d8-90884d3c0b40
        Total devices 2 FS bytes used 360.00KiB
        devid    1 size 20.00GiB used 1.28GiB path /dev/sdb
        devid    2 size 20.00GiB used 1.28GiB path /dev/sdc
```

查看balance任务是否完成  
[root@digoal ~]# `btrfs balance status -v /data01`
```
No balance found on '/data01'
```
还可继续转换，例如data想用raid0时  
[root@digoal ~]# `btrfs balance start -dconvert=raid0 /data01`
```
Done, had to relocate 1 out of 3 chunks
```
这里的chunks指的就是block group.


添加块设备并进行数据重分布，和前面的转换差不多，只是不改-d -m的profile。   
[root@digoal ~]#`btrfs device add -f /dev/sdd/data01`   
[root@digoal ~]#`btrfs device add -f /dev/sde/data01`   
[root@digoal ~]#`btrfs filesystem show /dev/sdb`   
```
Label: none  uuid: 165f59f6-77b5-4421-b3d8-90884d3c0b40
  Total    devices 4 FS bytes used 616.00KiB
  devid    1 size 20.00GiB used 1.28GiB path /dev/sdb
  devid    2 size 20.00GiB used 1.28GiB path /dev/sdc
  devid    3 size 20.00GiB used 0.00B path /dev/sdd
  devid    4 size 20.00GiB used 0.00B path /dev/sde
```
[root@digoal ~]# `btrfs balance start /data01`
```
Done, had to relocate 3 out of 3 chunks
```
[root@digoal ~]# `btrfs filesystem show /dev/sdb`
```
Label: none  uuid: 165f59f6-77b5-4421-b3d8-90884d3c0b40
  Total   devices 4 FS bytes used 1.29MiB
  devid    1 size 20.00GiB used 1.03GiB path /dev/sdb
  devid    2 size 20.00GiB used 1.03GiB path /dev/sdc
  devid    3 size 20.00GiB used 2.00GiB path /dev/sdd
  devid    4 size 20.00GiB used 2.00GiB path /dev/sde
```

将metadata转换为raid10存储，重分布  
[root@digoal ~]# `btrfs balance start -mconvert=raid10 /data01`
```
Done, had to relocate 2 out of 3 chunks
```
[root@digoal ~]# `btrfs filesystem show /dev/sdb`
```
Label: none  uuid: 165f59f6-77b5-4421-b3d8-90884d3c0b40
  Total   devices 4 FS bytes used 1.54MiB
  devid    1 size 20.00GiB used 1.53GiB path /dev/sdb
  devid    2 size 20.00GiB used 1.53GiB path /dev/sdc
  devid    3 size 20.00GiB used 1.53GiB path /dev/sdd
  devid    4 size 20.00GiB used 1.53GiB path /dev/sde
```
查看重分布后的三种类型的使用量  
[root@digoal ~]# `btrfs filesystem df /data01`
```
Data, RAID0: total=4.00GiB, used=1.25MiB
System, RAID10: total=64.00MiB, used=4.00KiB
Metadata, RAID10: total=1.00GiB, used=36.00KiB
GlobalReserve, single: total=4.00MiB, used=0.00B
```
 
删除块设备（必须确保达到该profile级别最小个数的块设备）  
[root@digoal ~]#` btrfs filesystem df /data01`
```
Data, RAID10: total=2.00GiB, used=1.00GiB
System, RAID10: total=64.00MiB, used=4.00KiB
Metadata, RAID10: total=1.00GiB, used=1.18MiB
GlobalReserve, single: total=4.00MiB, used=0.00B
```
[root@digoal ~]# `btrfs filesystem show /data01`
```
Label: none  uuid: 165f59f6-77b5-4421-b3d8-90884d3c0b40
  Total devices 4 FS bytes used 1.00GiB
  devid    1 size 20.00GiB used 1.53GiB path /dev/sdb
  devid    2 size 20.00GiB used 1.53GiB path /dev/sdc
  devid    3 size 20.00GiB used 1.53GiB path /dev/sdd
  devid    4 size 20.00GiB used 1.53GiB path /dev/sde
```
因为raid10至少需要4个块设备，所以删除失败  
[root@digoal ~]# `btrfs device delete /dev/sdb /data01`
```
ERROR: error removing device '/dev/sdb': unable to go below four devices on raid10
```
先转换为raid1，再演示  
[root@digoal ~]# `btrfs balance start -mconvert=raid1 -dconvert=raid1 /data01`
```
Done, had to relocate 3 out of 3 chunks
```
[root@digoal ~]#`btrfs filesystem df /data01`
```
Data, RAID1: total=2.00GiB, used=1.00GiB
System, RAID1: total=32.00MiB, used=4.00KiB
Metadata, RAID1: total=1.00GiB, used=1.11MiB
GlobalReserve, single: total=4.00MiB, used=0.00B
[root@digoal ~]# btrfs filesystem show /data01
Label: none  uuid: 165f59f6-77b5-4421-b3d8-90884d3c0b40
  Total   devices 4 FS bytes used 1.00GiB
  devid    1 size 20.00GiB used 1.03GiB path /dev/sdb
  devid    2 size 20.00GiB used 2.00GiB path /dev/sdc
  devid    3 size 20.00GiB used 2.00GiB path /dev/sdd
  devid    4 size 20.00GiB used 1.03GiB path /dev/sde
```
raid1最少只需要2个块设备，所以可以删除两个  
[root@digoal ~]#`btrfs device delete /dev/sdb /data01`
[root@digoal ~]#`btrfs device delete /dev/sdc /data01`
[root@digoal ~]#`btrfs filesystem df /data01`
```
Data, RAID1: total=2.00GiB, used=1.00GiB
System, RAID1: total=32.00MiB, used=4.00KiB
Metadata, RAID1: total=256.00MiB, used=1.12MiB
GlobalReserve, single: total=4.00MiB, used=0.00B
```
[root@digoal ~]# `btrfs filesystem show /data01`
```
Label: none  uuid: 165f59f6-77b5-4421-b3d8-90884d3c0b40
  Total   devices 2 FS bytes used 1.00GiB
  devid    3 size 20.00GiB used 2.28GiB path /dev/sdd
  devid    4 size 20.00GiB used 2.28GiB path /dev/sde
```
继续删除则失败  
[root@digoal ~]#`btrfs device delete /dev/sdd /data01`
```
ERROR: error removing device '/dev/sdd': unable to go below two devices on raid1
```
再加回去  
[root@digoal ~]# `btrfs device add /dev/sdb /data01`  
[root@digoal ~]# `btrfs device add /dev/sdc /data01`  
[root@digoal ~]# `btrfs balance start /data01`  
```
Done, had to relocate 4 out of 4 chunks
```
转换为raid5  
[root@digoal ~]#`btrfs balance start -mconvert=raid5 -dconvert=raid5 /data01`
```
Done, had to relocate 4 out of 4 chunks
```

可以删除1个，因为raid5最少需要3个块设备  
[root@digoal ~]# `btrfs device delete /dev/sde /data01`  
[root@digoal ~]# `btrfs filesystem df /data01`  
```
Data, RAID5: total=2.00GiB, used=1.00GiB
System, RAID5: total=64.00MiB, used=4.00KiB
Metadata, RAID5: total=1.00GiB, used=1.12MiB
GlobalReserve, single: total=4.00MiB, used=0.00B
```
[root@digoal ~]# `btrfs filesystem show /data01`
```
Label: none  uuid: 165f59f6-77b5-4421-b3d8-90884d3c0b40
  Total   devices 3 FS bytes used 1.00GiB
  devid    3 size 20.00GiB used 1.53GiB path /dev/sdd
  devid    5 size 20.00GiB used 1.53GiB path /dev/sdb
  devid    6 size 20.00GiB used 1.53GiB path /dev/sdc
```

## 附
透明压缩   
[root@localhost ~]#`mount -o compress={lzo|zlib} <device> <point>`  
创建快照    
[root@localhost ~]#`btrfs subvolume snapshot <pathname> <snap_pathname>`  
查看特定目录下的快照及子卷的信息    
[root@localhost ~]#`btrfs subvolume list 'pathname'`  

创建快照  
[root@localhost ~]#`btrfs subvolume snapshot /btrdata/mydata /btrdata/mydata_snapshot`  
```
Create a snapshot of '/btrdata/mydata' in '/btrdata/mydata_snapshot'  
```
[root@localhost ~]# `cat /btrdata/mydata/1.txt`  
```
1
```
[root@localhost ~]# `echo 'just a test' >> /btrdata/mydata/1.txt`  
[root@localhost ~]# `cat /btrdata/mydata/1.txt`  
```
1
just a test
```
[root@localhost ~]# `cat /btrdata/mydata_snapshot/1.txt`  
```
1
```
