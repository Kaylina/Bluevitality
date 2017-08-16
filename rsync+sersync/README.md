# 关于 Rsync+Sersync


## 使用说明
将文件夹下载到Linux主机后，修改.sh脚本文件：**Script.sh**

```shell
#define Server
	serv_pub_module=rsync
	serv_pub_dir=/data/nginx/sharefile	#S端共享目录 - 备份用
	serv_pub_user=rsync			#Rsync服务访问账号
	serv_pub_pass=12345			#Rsync服务访问密码
	serv_log_path=/var/log/rsyncd.log	#Rsync服务日志位置
	serv_Src_ACL=*				#源限制，格式：10.10.10.0/24或：10.10.10.*

#define Agent
	agen_watch_dir=/data/nginx/sharefile	#C端监视目录
	agen_rsync_user=rsync			#Rsync服务访问账号
	agen_rsync_pass=12345			#Rsync服务访问密码
	t_num=2					#Rsync同步线程数量（多核情况下适当调高）
	rsync_sevip=192.168.126.156		#Rsync服务ip
	rsync_module=rsync			#Rsync服务模块名称(需要与serv_pub_module的值相同)
```
## 执行：
直接执行.sh脚本文件：**Script.sh** 即可，会有case选项的提示，2个提示分别用于c/s模式 ..

c/s端的服务均写入了 /etc/rc.local 开机自启 ..

默认Sersync端的线程数量为 2

