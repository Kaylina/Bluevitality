
#### Example
```bash
~ #]vim /etc/udev/rules.d/<number>.rules
KERNEL==sd*, PROGRAM=/lib/udev/scsi_id -g -s %p, RESULT==123456, SYMLINK=%k_%c
#若有一个内核设备名称以 sd 开头，且 SCSI ID 为 123456，则为设备文件产生符号链接: "sda_123456"

KERNEL==”*”, OWNER=”root” GROUP=”root”, MODE=”0600″
#匹配任意被内核识别到的设备，然后设定这些设备的属组是root，组是root，访问权限模式是0600(-rw——-)
#这也是一个安全的缺省设置保证所有的设备在默认情况下只有root可以读写

KERNEL==”tty”, NAME=”%k”, GROUP=”tty”, MODE=”0666″, OPTIONS=”last_rule”
#匹配终端设备(tty)，然后设置新的权限为0600，所在的组是tty。它也设置了一个特别的设备文件名:%K
#在这里例子里，%k代表设备的内核名字。意味着内核识别出设备是什么名字，就创建什么样的设备文件名

KERNEL==”scd[0-9]*”, SYMLINK+=”cdrom cdrom-%k”
#表示 SCSI CD-ROM 驱动. 它创建一对设备符号连接：cdrom和cdrom-%k
#注意：仅仅第一行的NAME描述是有效的，后面的均忽略。  
#如果你想使用使用两个以上的名字来访问一个设备的话，可以考虑SYMLINK键。
#SYMLINK为 /dev/下的设备文件产生符号链接。由于 udev 只能为某个设备产生一个设备文件，
#所以为了不覆盖系统默认的 udev 规则所产生的文件，推荐使用符号链接。
    
KERNEL==”hd[a-z]”, BUS==”ide”, SYSFS{removable}==”1″, SYSFS{device/media}==”cdrom”, SYMLINK+=”cdrom cdrom-%k”
#表示ATA CDROM驱动器。这个规则创建和上面的规则相同的符号连接。ATA
#CDROM驱动器需要sysfs值以来区别别的ATA设备，因为SCSI CDROM可以被内核唯一识别。

KERNEL==”sd[b-z]”,RUN+=”/usr/local/bin/myprogram %k”
#表示识别出sdb、sdc…sdz设备的时候，运行外部程序/usr/local/bin/myprogram
#并将%k这个udev的操作符作为一个环境变量传给该程序作为一个选项。
#要注意的是udev不会在任何活动的terminal下运行这些外部程序，
#并且不会在shell上下文环境去执行（也就是说既有shell环境的变量如PATH、HOME等不会传递给该程序文件）
#所以你的程序必须是具有可执行权限（chmod +x），如果是一个shell脚本，那么必须具有shebang标示

ACTION==”add”, SUBSYSTEM==”scsi_device”, RUN+=”/sbin/modprobe sg”
#它告诉udev增加 /sbin/modprobe sg
#到命令列表，当任意SCSI设备增加到系统后，这些命令将执行。
#其效果就是计算机应该会增加sg内核模块来侦测新的SCSI设备。

SUBSYSTEM==”block”, ATTR{size}==”234441873”,SYMLINK+=”mydisk”
#表示识别sysfs属性，子系统是block，同时该设备的size为234441873，将为该设备创建符号链接mydisk
#ATTR{size}可以通过cat /sys/block/<device>/size查看，SUBSYSTEM可以通过udevadm info –a –p %p查看

KERNEL==”hdc”,SYMLINK+=”cdrom cdrom0”
#表示创建两个符号链接/dev/cdrom和/dev/cdrom0指向同一个设备即/dev/hdc
```

#### 关键字
|键|含义|
|--:|:---|
|ACTION      |   事件 (uevent) 的行为，例如：add( 添加设备 )、remove( 删除设备 )|
|KERNEL      |   在内核里看到的设备名字，比如sd*表示任意SCSI磁盘设备|
|DEVPATH     |  内核设备录进，比如/devices/*|
|SUBSYSTEM   |    子系统名字，例如：sda 的子系统为 block|
|BUS         |总线的名字，比如IDE,USB|
|DRIVER      |   设备驱动的名字，比如ide-cdrom|
|ID          | 独立于内核名字的设备名字|
|SYSFS{ value}|       sysfs属性值，他可以表示任意|
|ENV{ key}    |   环境变量，可以表示任意|
|PROGRAM      | 可执行的外部程序，如果程序返回0值，该键则认为为真(true)|
|RESULT       |  上一个PROGRAM调用返回的标准输出。|
|NAME         |根据这个规则创建的设备文件的文件名|
|OWNER       |  设备文件的属组|
|GROUP       |  设备文件所在的组。|
|MODE        | 设备文件的权限，采用8进制|
|RUN         |为设备而执行的程序列表|
|LABEL       |  在配置文件里为内部控制而采用的名字标签(下下面的GOTO服务)|
|GOTO        | 跳到匹配的规则（通过LABEL来标识），有点类似程序语言中的GOTO|
|IMPORT{ type} |    导入一个文件或者一个程序执行后而生成的规则集到当前文件|
|WAIT_FOR_SYSFS|   等待一个特定的设备文件的创建。主要是用作时序和依赖问题。|
|PTIONS        | 特定的选项|
|last_rule |对这类设备终端规则执行|
|ignore_device |忽略当前规则|
|ignore_remove |忽略接下来的并移走请求|
|all_partitions| 为所有的磁盘分区创建设备文件|

|**替换操作符**|键说明|
|--:|:---|
|\$kernel, %k|设备的内核设备名称，例如：sda、cdrom|
|\$number, %n|设备的内核号码，例如：sda3 的内核号码是 3|
|\$devpath, %p|设备的 devpath路径|
|\$id, %b|设备在 devpath里的 ID 号|\$sysfs{file}| 
|\$env{key}, %E{key}|一个环境变量的值|
|\$major, %M|设备的 major 号|
|\$minor %m|设备的 minor 号|
|\$result, %c|PROGRAM 返回的结|
|\$parent, %P|父设备的设备文件名|
|\$root, %r|udev_root的值，默认是 /dev/|
|\$tempnode, %N|临时设备名|
|%s\{file\}|设备sysfs里file的内容。即设备属性。如：\$sysfs{size} 表示该设备大小|
|%%|符号 % 本身|
|$$|符号 $ 本身|

| 操作符|     匹配or赋值|                        解释|
|:---:|:---:|:---|
|==     |       匹配     |        相等比较|
|!=     |       匹配     |       不等比较|
|=      |      赋值      |       分配一个特定的值给该键，他可以覆盖之前的赋值。|
|+=     |     赋值       |      追加特定的值给已经存在的键|
|:=     |       赋值     |            分配一个特定的值给该键，后面的规则不可能覆盖它|

重新启动UDEV：start_udev  

#### devadm info -ap /sys/block/sda  
打印出设备总线的所有位置的父子关系  
```bash
dm814x:~ ]# udevadm info -a -p /sys/block/sda
Udevadm info starts with the device specified by the devpath and then
walks up the chain of parent devices. It prints for every device
found, all possible attributes in the udev rules key format.
A rule to match, can be composed by the attributes of the device
and the attributes from one single parent device.
  looking at device '/devices/platform/omap/ti81xx-usbss/musb-hdrc.0/usb1/1-1/1-1:1.0/host1/target1:
  0:0/1:0:0:0/block/sda':  //总线路径和子路径.子路径好像不准确会变.
    KERNEL=="sda"
    SUBSYSTEM=="block"
    DRIVER==""
    ATTR{range}=="16"
    ATTR{ext_range}=="256"
    ATTR{removable}=="0"          //设备热插拔,0为不能,1为能.
    ATTR{ro}=="0"
    ATTR{size}=="976773168"
    ATTR{alignment_offset}=="0"
    ATTR{discard_alignment}=="0"
    ATTR{capability}=="50"
    ATTR{stat}=="     9     26    280     90      0      0      0      0      0     90     90"
    ATTR{inflight}=="       0        0"
  looking at parent device '/devices/platform/omap/ti81xx-usbss/musb-hdrc.0/usb1/1-1/1-1:1.0
  /host1/target1:0:0/1:0:0:0':
    KERNELS=="1:0:0:0"
    SUBSYSTEMS=="scsi"
    DRIVERS=="sd"
    ATTRS{device_blocked}=="0"
    ATTRS{type}=="0"
    ATTRS{scsi_level}=="3"
    ATTRS{vendor}=="Hitachi "           //硬盘牌子,如日立
    ATTRS{model}=="HTS547550A9E384 "
    ATTRS{rev}=="    "
    ATTRS{state}=="running"
    ATTRS{timeout}=="30"
    ATTRS{iocounterbits}=="32"
    ATTRS{iorequest_cnt}=="0x21"
    ATTRS{iodone_cnt}=="0x21"
    ATTRS{ioerr_cnt}=="0x0"
    ATTRS{evt_media_change}=="0"
    ATTRS{dh_state}=="detached"
    ATTRS{queue_depth}=="1"
    ATTRS{queue_type}=="none"
    ATTRS{max_sectors}=="240"
  looking at parent device '/devices/platform/omap/ti81xx-usbss/musb-hdrc.0/usb1/1-1/1-1:1.0
  /host1/target1:0:0':
    KERNELS=="target1:0:0"
    SUBSYSTEMS=="scsi"
    DRIVERS==""
  looking at parent device '/devices/platform/omap/ti81xx-usbss/musb-hdrc.0/usb1/1-1/1-1:1.0/host1':
    KERNELS=="host1"
    SUBSYSTEMS=="scsi"
    DRIVERS==""
  looking at parent device '/devices/platform/omap/ti81xx-usbss/musb-hdrc.0/usb1/1-1/1-1:1.0':
    KERNELS=="1-1:1.0"
    SUBSYSTEMS=="usb"
    DRIVERS=="usb-storage"
    ATTRS{bInterfaceNumber}=="00"
    ATTRS{bAlternateSetting}==" 0"
    ATTRS{bNumEndpoints}=="02"
    ATTRS{bInterfaceClass}=="08"
    ATTRS{bInterfaceSubClass}=="06"
    ATTRS{bInterfaceProtocol}=="50"
    ATTRS{supports_autosuspend}=="1"
    ATTRS{interface}=="MSC Bulk-Only Transfer"
  looking at parent device '/devices/platform/omap/ti81xx-usbss/musb-hdrc.0/usb1/1-1':
    KERNELS=="1-1"
    SUBSYSTEMS=="usb"
    DRIVERS=="usb"
    ATTRS{configuration}=="USB Mass Storage"
    ATTRS{bNumInterfaces}==" 1"
    ATTRS{bConfigurationValue}=="1"
    ATTRS{bmAttributes}=="c0"
    ATTRS{bMaxPower}=="  2mA"
    ATTRS{urbnum}=="14636"
    ATTRS{idVendor}=="152d"
    ATTRS{idProduct}=="2352"
    ATTRS{bcdDevice}=="0100"
    ATTRS{bDeviceClass}=="00"
    ATTRS{bDeviceSubClass}=="00"
    ATTRS{bDeviceProtocol}=="00"
    ATTRS{bNumConfigurations}=="1"
    ATTRS{bMaxPacketSize0}=="64"
    ATTRS{speed}=="480"
    ATTRS{busnum}=="1"
    ATTRS{devnum}=="2"
    ATTRS{devpath}=="1"
    ATTRS{version}==" 2.00"
    ATTRS{maxchild}=="0"
    ATTRS{quirks}=="0x0"
    ATTRS{avoid_reset_quirk}=="0"
    ATTRS{authorized}=="1"
    ATTRS{manufacturer}=="JMicron"         //硬盘主控芯片牌子:JMicron
    ATTRS{product}=="USB to ATA/ATAPI Bridge"                //总线协议
    ATTRS{serial}=="2170052CDDFF"
  looking at parent device '/devices/platform/omap/ti81xx-usbss/musb-hdrc.0/usb1':
    KERNELS=="usb1"
    SUBSYSTEMS=="usb"
    DRIVERS=="usb"
    ATTRS{configuration}==""
    ATTRS{bNumInterfaces}==" 1"
    ATTRS{bConfigurationValue}=="1"
    ATTRS{bmAttributes}=="e0"
    ATTRS{bMaxPower}=="  0mA"
    ATTRS{urbnum}=="32"
    ATTRS{idVendor}=="1d6b"
    ATTRS{idProduct}=="0002"
    ATTRS{bcdDevice}=="0206"
    ATTRS{bDeviceClass}=="09"
    ATTRS{bDeviceSubClass}=="00"
    ATTRS{bDeviceProtocol}=="00"
    ATTRS{bNumConfigurations}=="1"
    ATTRS{bMaxPacketSize0}=="64"
    ATTRS{speed}=="480"
    ATTRS{busnum}=="1"
    ATTRS{devnum}=="1"
    ATTRS{devpath}=="0"
    ATTRS{version}==" 2.00"
    ATTRS{maxchild}=="1"
    ATTRS{quirks}=="0x0"
    ATTRS{avoid_reset_quirk}=="0"
    ATTRS{authorized}=="1"
    ATTRS{manufacturer}=="Linux 2.6.37+ musb-hcd"
    ATTRS{product}=="MUSB HDRC host driver"
    ATTRS{serial}=="musb-hdrc.0"
    ATTRS{authorized_default}=="1"
  looking at parent device '/devices/platform/omap/ti81xx-usbss/musb-hdrc.0':
    KERNELS=="musb-hdrc.0"
    SUBSYSTEMS=="platform"
    DRIVERS=="musb-hdrc"
    ATTRS{mode}=="a_host"
    ATTRS{vbus}=="Vbus off, timeout 1100"
  looking at parent device '/devices/platform/omap/ti81xx-usbss':
    KERNELS=="ti81xx-usbss"
    SUBSYSTEMS=="platform"
    DRIVERS=="ti81xx-usbss"
  looking at parent device '/devices/platform/omap':
    KERNELS=="omap"
    SUBSYSTEMS==""
    DRIVERS==""
  looking at parent device '/devices/platform':
    KERNELS=="platform"
    SUBSYSTEMS==""
    DRIVERS==""
```
