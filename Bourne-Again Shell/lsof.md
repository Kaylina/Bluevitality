#### 说明
``` bash
# lsof（list open files）是一个列出当前系统打开文件的工具。
# 在linux下任何事物都以文件的形式存在!，通过文件不仅可访问常规数据，还可以访问网络连接和硬件。
# 如传输控制协议 (TCP) 和用户数据报协议 (UDP) 套接字等，系统在后台都为该应用程序分配了一个文件描述符。
# 无论这个文件的本质如何，该文件描述符为应用程序与基础操作系统之间的交互提供了通用接口。
# 因为应用程序打开文件的描述符列表提供了大量关于这个应用程序本身的信息，因此通过lsof能够查看，这个列表对系统监测以及排错将是很有帮助的。


[root@localhost ~]# lsof | head -n 5
COMMAND    PID  TID           USER   FD      TYPE             DEVICE  SIZE/OFF       NODE NAME
systemd      1                root  cwd       DIR              253,0      4096        128 /
systemd      1                root  rtd       DIR              253,0      4096        128 /
systemd      1                root  txt       REG              253,0   1482272  101411655 /usr/lib/systemd/systemd
systemd      1                root  mem       REG              253,0     20040   67257837 /usr/lib64/libuuid.so.1.3.0
[root@localhost ~]# lsof -i :22
COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
sshd    1043 root    3u  IPv4  20560      0t0  TCP *:ssh (LISTEN)
sshd    1043 root    4u  IPv6  20562      0t0  TCP *:ssh (LISTEN)
^C
[root@localhost ~]# lsof -u root | head -n 5
COMMAND    PID USER   FD      TYPE             DEVICE  SIZE/OFF       NODE NAME
systemd      1 root  cwd       DIR              253,0      4096        128 /
systemd      1 root  rtd       DIR              253,0      4096        128 /
systemd      1 root  txt       REG              253,0   1482272  101411655 /usr/lib/systemd/systemd
systemd      1 root  mem       REG              253,0     20040   67257837 /usr/lib64/libuuid.so.1.3.0

#COMMAND：进程名称
#PID：进程ID
#USER：所有者
#FD：文件描述符，应用程序通过文件描述符识别该文件。如cwd、txt等
#TYPE：文件类型，如DIR、REG等
#DEVICE：指定磁盘的名称
#SIZE：文件大小
#NODE：索引节点（文件在磁盘上的标识）
#NAME：打开文件的确切名称
```

#### Example
```bash
lsof filename         #显示开启filename文件的进程
lsof -c program       #显示program进程现在打开的文件
lsof -c -p 1234       #列出进程号为1234的进程所打开的文件
lsof -u 1000          #查看uid是100的用户的进程的文件使用情况
lsof -g gid           #显示归属gid的进程情况
lsof +d /usr/local/         #列出指定目录被进程开启的文件
lsof +D /usr/local/         #同上，但会搜索目录下的目录，时间较长（包括子目录）
lsof -c courier -u ^samba   #显示出那些文件被以courier打头的进程打开，但并不属于用户samba的
lsof -i           #显示所有打开的端口
lsof -i:80        #显示所有打开80端口的进程
lsof | grep -i DELETE       #查看已经被删除但文件句柄仍被应用打开的僵尸信息（常用）
```
