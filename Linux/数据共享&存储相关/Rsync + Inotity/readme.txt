Rsync v3.1.0 安装说明

用途：多台Linux Server之间的数据同步

1、安装方式
编译安装

2、安装文件
Install.sh	Rsync源码编译安装
inotify.sh	inotify-tools源码编译安装安装 ( 用于监控某目录内的变化，以及时触发rsync进行同步 )

3、安装目录
/usr/local/rsync

4、执行文件
/usr/local/rsync/bin/rsync
Pid: /usr/local/rsync/logs/rsyncd.pid

5、配置文件
5.1、文件目录
/usr/local/rsync/etc

5.2、主配置文件
/usr/local/rsync/etc/rsyncd.conf

5.3、用户配置文件 ( 帐号密码 )
/usr/local/rsync/etc/rsyncd.pass

6、日志文件
/usr/local/rsync/logs/rsyncd.log

7、控制命令
启动 : service rsyncd start
关闭 : service rsyncd stop
重启 : service rsyncd restart
状态 ：service rsyncd status

8、启动脚本：/etc/rc.d/init.d/rsyncd


附：
软件信息：
  group：nobody
  user： nobody

推送文件至某服务器：
	cd /www/xx
	rsync -arP --delete --password-file=/xx/user.pass --exclude-from=/xx/not_sync_list.txt * username@10.50.201.187::blockname

从某服务器上下载文件
	/usr/local/rsync/bin/rsync -azP --password-file=/xx/sitename.pass nman@10.50.201.98::video /www/
