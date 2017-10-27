#### 说明：
```txt
logger是个shell命令接口，可通过该接口使用Syslog的系统日志模块，还可从命令行直接向系统日志文件写入一行信息

参数：
-d, --udp  	  使用数据报(UDP)而不是使用默认的流连接(TCP)
-i, --id   	  逐行记录每一次logger的进程ID
-t， --tag tag			  指定标记记录
-p， --priority priority_level	  指定输入消息的优先级，可以是数字或 "facility.level" 格式，如："-p local3.info " 
-f, --file file_name	  记录特定的文件
-n， --server 		  写入指定的远程syslog服务器，使用UDP代替内装式syslog的例程
-P， --port port_num	  使用指定的UDP端口。默认的端口号是514
-s， --stderr			  输出标准错误到系统日志。
-u， --socket socket	    写入指定socket而不是到内置系统日志例程

facility：
	auth：   	用户授权
	authpriv：	授权和安全
	cron：   	计划任务
	daemon： 	系统守护进程
	kern：   	与内核有关的信息
	lpr      	与打印服务有关的信息
	mail     	与电子邮件有关的信息
	news     	来自新闻服务器的信息
	syslog   	由syslog生成的信息
	user     	用户的程序生成的信息，默认
	uucp     	由uucp生成的信息
	local0~7 	用来定义本地策略

level：
	alert 		需要立即采取动作
	crit  		临界状态
	debug 		调试
	emerg 		系统不可用
	err   		错误状态
	error 		错误状态
	info  		正常消息
	notice		正常但是要注意
```

#### Example：
```txt
service rsyslog restart

logger System Rebooted          #往系统日志例程中写入“System Rebooted”可在/var/log/syslog中查看

$ logger -f /var/log/myapp.log  #记录特定文件中的信息

$ logger -i -t "my_test" -p local3.notice "test_info" 
$ cat /var/log/my_test.log  
    May 5 21:27:37 gino-virtual-machine my_test[3651]: test_info

```
