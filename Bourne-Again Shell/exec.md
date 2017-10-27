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
exec ${@}
[root@localhost ~]# bash test.sh ls -lh   #脚本后接入的参数将被exec捕获并理解为命令进行解析执行
总用量 4.0K
-rw-r--r-- 1 root root 23 8月  15 10:47 test.sh


#find和exec
#在当前目录下(包含子目录)，查找所有txt文件并找出含有字符串"bin"的行
find ./ -name "*.txt" -exec grep "bin" {} \; 
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
```
