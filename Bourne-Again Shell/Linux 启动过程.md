<!-- TOC -->

- [Linux系统启动流程](#linux%E7%B3%BB%E7%BB%9F%E5%90%AF%E5%8A%A8%E6%B5%81%E7%A8%8B)
    - [一．BIOS自检](#%E4%B8%80%EF%BC%8Ebios%E8%87%AA%E6%A3%80)
    - [二．启动GRUB/LILO](#%E4%BA%8C%EF%BC%8E%E5%90%AF%E5%8A%A8grublilo)
    - [三．加载内核](#%E4%B8%89%EF%BC%8E%E5%8A%A0%E8%BD%BD%E5%86%85%E6%A0%B8)
    - [四．执行init进程](#%E5%9B%9B%EF%BC%8E%E6%89%A7%E8%A1%8Cinit%E8%BF%9B%E7%A8%8B)
    - [五．通过/etc/inittab文件进行初始化](#%E4%BA%94%EF%BC%8E%E9%80%9A%E8%BF%87etcinittab%E6%96%87%E4%BB%B6%E8%BF%9B%E8%A1%8C%E5%88%9D%E5%A7%8B%E5%8C%96)
        - [/etc/rc.d/rc.sysinit](#etcrcdrcsysinit)
        - [/etc/rc.d/rcX.d/[KS]](#etcrcdrcxdks)
        - [执行/etc/ec.d/rc.local](#%E6%89%A7%E8%A1%8Cetcecdrclocal)
    - [六．执行/bin/login程序](#%E5%85%AD%EF%BC%8E%E6%89%A7%E8%A1%8Cbinlogin%E7%A8%8B%E5%BA%8F)

<!-- /TOC -->

# Linux系统启动流程

下面是整个Linux系统的启动过程：

Linux Boot Step

Start   BIOS
        grub/lilo
        Kernel boot
        init      rc.sysinit
                  rc
        mingetty  login
        shell
        登录系统

## 一．BIOS自检

计算机在接通电源之后首先由BIOS进行POST自检，然后依据BIOS内设置的引导顺序从硬盘、软盘或CDROM中读入引导块。Linux系统是人BIOS中的地址oxFFFF0处开始引导的。BIOS的第1个步骤是加电POST自检。POST的工作是对硬件进行检测。BIOS的第2个步骤是进行本地设备的枚举和初始化。BIOS由两部分组成：POST代码和运行时的服务。当POST完成之后，它被从内存中清理出来，但是BIOS运行时服务依然保留在内存中，目标操作系统可以使用这些服务。

BIOS运行时会按照CMOS的设置定义的顺序来搜索处于活动状态并且可以引导的设备。引导设备可以是软盘、CD-ROM、硬盘上的某个分区、网络上的某个设备甚至是USB闪存。通常，Linux系统都是从硬盘上引导的，其中主引导记录（MBR）中包含主引导加载程序。MBR是一个512字节大小的扇区，位于磁盘上的第一个扇区（0道0柱面1扇区）。当MBR被加载到RAM中之后，BIOS就会将控制权交给MBR。

如果要查看MBR的内容，用户需要以root用户的身份运行如下命令：

dd if=/dev/had of=mbr.bin bs=512 count=1
读入了1+0个块
输出了1+0个块
od –xa mbr.bin
… …

它从/dev/had（第一个IDE盘）上读取前512个字节的内容，并将其写入mbr.bin文件中。od命令会以十六进制和ASCII码格式打印这个二进制文件的内容。

## 二．启动GRUB/LILO

GRUB和LILO都是引导加载程序。引导加载程序用于引导操作系统启动。当机器引导它的操作系统时，BIOS会读取引导介质上最前面的512字节（主引导记录）。在单一的MBR中只能存储一个操作系统的引导记录，所以当需要多个操作系统时就会出现问题，需要更灵活的引导加载程序。

所有引导加载程序都以类似的方式工作，满足共同的目的，但LILO和GRUB之间也有很多不同之处：

LILO没有交互式命令界面，而GRUB拥有；
LILO不支持网络引导，而GRUB支持；
LILO将可以引导操作系统的信息存储在MBR中。

如果修改了LILO配置文件，必须将LILO第一阶段引导加载程序重写到MBR。相对于GRUB，这是一个更为危险的选择，因为错误配置的MBR可能会让系统无法引导。使用GRUB时，如果配置文件配置错误，则只是默认转到GRUB命令行界面。

## 三．加载内核

接下来的步骤就是加载内核映像到内存中，内核映像并不是一个可执行的内核，而是一个压缩过的内核映像。通常它是一个zImage（压缩映像，小于512KB）或是一个bzImage（较大的压缩映像，大于512KB），它是提前使用zlib压缩过的。在这个内核映像前面是一个例程，它实现少量硬件设置，并对内核映像中包含的内核进行解压缩，然后将其放入高端内存中。如果有初始RAM磁盘映像，系统就会将它移动到内存中，并标明以后使用。然后该例程会调用内核，并开始启动内核引导的过程。

## 四．执行init进程

init进程是系统所有进程的起点，内核在完成核内引导以后，即在本进程空间内加载init程序，它的进程呈是1。Init进程是所有进程的发起者和控制者。因为在任何基于Linux的系统中，它都是第一个运行的进程，所以init进程的编号（PID）永远是1。

init进程有以下两个作用。

init进程的第一个作用是扮演终结父进程的角色。因为init进程永远不会被终止，所以系统总是可以确信它的存在，并在必要的时候以它为参照。如果某个进程在它衍生出来的全部子进程结束之前被终止，就会出现必须以init为参照的情况。此时那些失去了父进程的子进程就都会以init作为它们的父进程。

init的第二个作用是在进入某个特定的运行级别时运行相应的程序，以此对各种运行级别进行管理。它的这个作用是由/etc/inittab文件定义的。

## 五．通过/etc/inittab文件进行初始化

Init的工作是根据/etc/inittab来执行相应的脚本，进行系统初始化，如设置键盘、字体、装载模块，设置网络等。

### /etc/rc.d/rc.sysinit

在init的配置文件中有如下一行：
si::sysinit:/etc/rc.d/rc.sysinit

rc.sysinit是由init执行的第一个脚本，它主要完成一些系统初始化的工作。rc.sysinit是每一个运行级别都要首先运行的重要脚本，它主要完成的工作有：激活交换分区、检查磁盘、加载硬件模块以及其他一些需要优先执行的任务。/etc/rc.d/ rc.sysinit主要完成各个运行模式中相同的初始化工作。包括：

设置初始的$PATH变量；
配置网络；
为虚拟内存启动交换；
调协系统的主机名；
检查root文件系统，以进行必要的修复；
检查root文件系统的配额；
为root文件系统打开用户和组的配额；
以读/写的方式重新装载root文件系统；
清除被装载的文件系统表/etc/mtab；
把root文件系统输入到mtab；
使系统为装入模块做准备；
查找模块的相关文件；
检查文件系统，以进行必要的修复；
加载所有其他文件系统；
清除/etc/mtab、/etc/fastboot和/etc/nologin；
删除UUCP和lock文件；
删除过时的子系统文件；
删除过时的pid文件；
设置系统时钟；
激活交换分区；
初始化串行端口；
装入模块。



### /etc/rc.d/rcX.d/[KS]

在rc.sysinit执行后，将返回init，继续执行/etc/rc.d/rc程序。以运行级别5为例，init将执行配置文件inittab中的以下内容：
15:5:wait:/etc/rc.d/rc 5

这一行表示以5为参数运行/etc/rc.d/rc，/etc/rc.d/rc是一个shell脚本，它接受5作为参数，去执行/etc/rc.d/rc5.d目录下的所有的rc启动脚本，/etc/rc.d/rc5.d目录中的启动脚本实际上都是一些链接文件，而不是真正的rc启动脚本，真正的rc启动脚本实际上都在/etc/rc.d/init.d目录下。而这些rc启动脚本有着类似的用法，它们一般能接受stat、stop、restart、status等参数。

/etc/rc.d/rc5.d中的rc启动脚本通常是以K或S开头的链接文件，以S开头的启动脚本将以start参数来运行。如果发现相应的脚本也存在K打头的链接，而且已经处于运行状态了（以/var/lock/subsys下的文件作为标志），则将首先以stop为参数停止这些已经启动了的守护进程，然后再重新运行。这样做是为了保证当init改变运行级别时，所有相关的守护进程都将重启。

至于在每个运行级中将运行哪些守护进程，用户可以通过chkconfig来自行设定。常见的守护进程如下。

amd：自动安装NFS守护进程。
apmd：高级电源管理守护进程。
arpwatch：记录日志并构建一个在LAN接口上看到的以太网地址和IP地址对应的数据库。
outofs：自动安装管理进程automount，与NFS相关，依赖于NIS。
crond：Linux系统下计划任务的守护进程。
named：DNS服务器。
netfs：安装NFS、Samba和Netware网络文件系统。
network：激活已配置网络接口的脚本程序。
nfs：打开NFS服务。
portmap：RPCportmap管理器，它管理基于RPC服务的连接。
sendmail：邮件服务器sendmail。
smb：Samba文件共享/打印服务。
syslog：一个让系统引导时启动syslog和klogd系统日志守候进程的脚本。
xfs：X Window字型服务器，为本地和远程X服务器提供字型集。
Xinetd：支持多种网络服务的核心守护进程，可以管理wuftp、sshd、telnet等服务。

这些守护进程启动完毕，rc程序也就执行完了，然后又返回init继续下一步。



### 执行/etc/ec.d/rc.local

RHEL 4中的运行模式2、3、5都把/etc/rc.d/rc.local做为初始化脚本中的最后一个，所以用户可以自己在这个文件中添加一些需要在其他初始化工作之后、登录之前执行的命令。在维护Linux系统时一般会遇到需要系统管理员对开机或关机命令脚本进行修改的情况。如果所做的修改只在引导开机的时候起作用，并且改动不大的话，可以考虑简单地编辑一下/etc/rc.d/rc.local脚本。这个命令脚本程序是在引导过程的最后一步被执行的。

## 六．执行/bin/login程序

login程序会提示使用者输入账号及密码，接着编码并确认密码的正确性，如果账号与密码相符，则为使用者初始化环境，并将控制权交给shell，即等待用户登录。

login会接收mingetty传来的用户名作为用户名参数，然后login会对用户名进行分析。如果用户名不是root，且存在/etc/nologin文件，login将输出nologin文件的内容，然后退出。这通常用来在系统维护时防止非root用户登录。只有在/etc/securetty中登记了的终端才允许root用户登录，如果不存在这个文件，则root可以在任何终端上登录。/etc/usertty文件用于对用户作出附加访问限制，如果不存在这个文件，则没有其他限制。

在分析完用户名后，login将搜索/etc/passwd以及/etc/shadow来验证密码以及设置账户的其他信息，比如：主目录什么、使用何种shell。如果没有指定主目录，则将主目录默认设置为根目录；如果没有指定shell，则将shell类型默认设置为/bin/bash。

Login程序成功后，会向对应的终端再输出最近一次登录的信息（在/var/log/lostlog中有记录），并检查用户是否有新邮件（在/usr/spool/mail的对应用户名目录下），然后开始设置各种环境变量。对于bash来说，系统首先寻找/etc/profile脚本文件并执行它；然后如果用户的主目录中存在.bash_profile文件，就执行它，在这些文件中又可能调用了其他配置文件，所有的配置文件执行后，各种环境变量也设好了，这时会出现大家熟悉的命令行提示符，至此整个启动过程就结束了。
