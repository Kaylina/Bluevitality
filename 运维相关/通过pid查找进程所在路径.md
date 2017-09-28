> proc内进程pid的exe目录内存放着本进程所对应的磁盘文件的软连接信息...

过滤出网络进程的pid信息：`netstat -atupnl | grep java`
通过此pid信息查找其路径：`ls /proc/$pid/exe`