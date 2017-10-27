#### 说明
```txt
对Linux而言所有对设备&文件的操作都使用文件描述符来进行的!
文件描述符是个非负的整数，它是一个索引值，并指向内核中每个进程打开文件的记录表
当打开一个现存文件或创建新文件时内核就向进程返回一个文件描述符
当需要读写文件时也需要把文件描述符作为参数传递给相应的函数
通常一个进程启动时都会打开3个文件:
0 标准输入
1 标准输出
2 标准出错处理

查看和设置LINUX能够打开的文件描述符数：
ulimit -n
ulimit -n 1024
```
#### 使用`exec "command"`替代其父进程上下文环境
```bash
[root@localhost ~]# cat test.sh 
#!/bin/bash
exec ${@}     #原进程的代码段，数据段，堆栈段被新的进程所代替。
[root@localhost ~]# bash test.sh ls -lh   #脚本后接入的参数将被exec捕获并理解为命令进行解析执行
总用量 4.0K
-rw-r--r-- 1 root root 23 8月  15 10:47 test.sh


#find和exec
#在当前目录下(包含子目录)，查找所有txt文件并找出含有字符串"bin"的行
find ./ -name "*.txt" -exec grep "bin" {} \; 

# exec与system的区别：
# exec是直接用新的进程去代替原来的程序运行，运行完毕之后不回到原先的程序中去。
# system是调用shell执行你的命令，system=fork+exec+waitpid,执行完毕之后，回到原先的程序中去。继续执行下面的部分。
# exec常用来替代当前 shell 并重新启动一个 shell
```
#### 调整文件描述符
```bash
[root@localhost ~]# exec 6> /etc/file2          #创建描述符6对应的文件
[root@localhost ~]# exec 6>&-                   #关闭指定描述符
[root@localhost ~]# exec 3<> hello.txt          #以读写方式绑定到文件描述符"3"
[root@localhost ~]# echo "hello exec" >&3       #向文件描述符3写入"hello exec"
[root@localhost ~]# echo "hello world" >&3      #写入"hello world“（覆盖）
[root@localhost ~]# exec 3>&-                   #关闭写，然而它也不能读了，若是 exec 3<&- 则关闭读，同时也不能写了

#将标准输出重定向
[root@localhost ~]# exec 1>hello.txt            #将标准输出重定向到文件hello.txt，从此以后脚本的输出都将被写入hello.txt
[root@localhost ~]# echo "hello exec"
[root@localhost ~]# echo "hello world"

#输入重定向
[root@localhost ~]# exec 100<&0
[root@localhost ~]# exec < hello.txt
[root@localhost ~]# read line1
[root@localhost ~]# echo $line1
[root@localhost ~]# read line2
[root@localhost ~]# echo $line2
[root@localhost ~]# exec 0<&100 100>&-          #恢复默认标准输出并关闭文件描述符100
[root@localhost ~]# read custom

#查看特定PID的文件描述符
[root@localhost tmp]# ls /proc/818/fd
3  4  7

#从文件描述符读取4个字符
[root@localhost tmp]# read -n 4 <&3    

#代码块重定向
#!/bin/bash
{
  command .... ; command ... ; command ...
} 1> record.log 2>&1

#注：
# tee是在不影响原本 I/O 的情况下，将 stdout 复制一份到档案去
# n<&-        关闭输入文件描述符n
# n>&-        关闭输出文件描述符n.
# 0<&-, <&-   关闭stdin
# 1>&-, >&-   关闭stdout
```
## mkfifo
```说明
mkfifo会创建FIFO特殊文件（文件类型为p），它是个命名管道（可用来做进程间通信的桥梁）
管道也是一种文件，一般是linux中的一个页大小，4k，管道数据一旦被读取就没了。另外，管道是单方向的
```
#### Example
```bash
#窗口1
[root@localhost tmp]# mkfifo tmp.fifo           #创建管道
[root@localhost tmp]# ls -l tmp.fifo            #可看到文件类型：p
prw-r--r-- 1 root root 0 8月  15 17:41 tmp.fifo
[root@localhost tmp]# ls -l > tmp.fifo          #执行ls进程并将结果写入管道，此时若其他进程未读此管道内容则一直被阻塞！

#窗口2
[root@localhost tmp]# cat tmp.fifo              #因为被阻塞住了，所以在另一个窗口用cat读取管道内容，此时窗口1将执行完毕
总用量 0
prw-r--r-- 1 root root 0 8月  15 17:41 tmp.fifo
```
