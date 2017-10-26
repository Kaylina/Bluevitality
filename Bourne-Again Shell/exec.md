#### 取代父进程
```bash
[root@localhost ~]# cat test.sh 
#!/bin/bash

exec ${@}
[root@localhost ~]# bash test.sh ls -lh
总用量 4.0K
-rw-r--r-- 1 root root 23 8月  15 10:47 test.sh
```
#### 调整文件描述符
```bash
[root@localhost ~]# exec 6> /etc/file2  #创建描述符6对应的文件
[root@localhost ~]# exec 6>&-           #关闭指定描述符
```
