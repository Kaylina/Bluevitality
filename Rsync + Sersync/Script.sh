#!/bin/bash

#define Server
	serv_pub_module=rsync
	serv_pub_dir=/data/nginx/sharefile			#S端共享目录 - 备份用
	serv_pub_user=rsync					#Rsync服务访问账号
	serv_pub_pass=12345					#Rsync服务访问密码
	serv_log_path=/var/log/rsyncd.log			#Rsync服务日志位置
	serv_Src_ACL=*						#源IP限制，格式：192.168.10.0/24或：192.168.1.*

#define Agent
	agen_watch_dir=/data/nginx/sharefile			#C端监视目录
	agen_rsync_user=rsync					#Rsync服务访问账号
	agen_rsync_pass=12345					#Rsync服务访问密码
	t_num=2							#Rsync同步线程数量（多核情况下适当调高）
	rsync_sevip=192.168.126.156				#Rsync服务ip
	rsync_module=rsync					#Rsync服务模块名称(需要与serv_pub_module的值相同)

#----------------------------------------------------------------------------------------------------------------------

#define sofrware function ...
function install_rsync() {

	tar zxf rsync-3.1.1.tar.gz && cd rsync-3.1.1
	./configure ; make && make install
	cd - 
	return 0
	
}

function install_inotify() {

	tar zxf inotify-tools-3.14.tar.gz && cd inotify-tools-3.14
	./configure --prefix=/usr/local/inotify ; make && make install
	cd - 
	return 0
	
}

function install_sersync() {

	tar zxf sersync2.5.4_64bit_binary_stable_final.tar.gz
	mv ./GNU-Linux-x86 /usr/local/sersync
	cd /usr/local/sersync
	echo "${agen_rsync_pass:=12345}" > /usr/local/sersync/user.pass
	chmod 600 /usr/local/sersync/user.pass
	cd - 
	return 0
	
}

function selinux_config() {

	setenforce 0
	sed -i "s/^SELINUX=.*/SELINUX=disabled/g" /etc/selinux/config 
	echo -n "SElinux："
	grep -oP "(?<=^SELINUX=).*" /etc/selinux/config
	
}

function serv_config() {
	
	selinux_config
	install_rsync && echo -e "\033[32mRsync'Server dameon install success... \033[0m"

cat > /etc/rsyncd.conf <<eof
uid=root
gid=root
pidfile = /var/run/rsyncd.pid
max connections = 36000
use chroot = no
log file=${serv_log_path}
ignore errors = yes
read only = no
auth users=${serv_pub_user}
secrets file = /etc/rsync.pass
hosts allow =${serv_Src_ACL}
#hosts deny = *
timeout = 600
[${serv_pub_module:=rsync}]
comment=rsync
path=${serv_pub_dir}
eof

	echo "${serv_pub_user}:${serv_pub_pass}" > /etc/rsync.pass
	touch ${serv_log_path}
	chmod 600 /etc/{rsyncd.conf,rsync.pass} ; chmod 755 ${serv_pub_dir}
	rm -rf /var/run/rsyncd.pid
	/usr/local/bin/rsync --daemon
	
	netstat -atupnl | grep -q 873  &&  {
		echo -e "\033[32mRsync'Server dameon start success... \033[0m"
		echo "/usr/local/bin/rsync --daemon" >> /etc/rc.local
	}  ||  {
		pkill rsync ; /usr/local/bin/rsync --daemon
		netstat -atupnl | grep -q 873 ; [ "$?" -ne "0" ] && echo -e "\033[31mRsync'Server dameon start Fail... \033]0m"
		exit 1
	}
}

function agen_config() {

	selinux_config
	install_rsync && install_inotify && install_sersync && echo -e "\033[32mRsync'Client dameon install success... \033[0m"

echo "fs.inotify.max_queued_events=99999999" >>  /etc/sysctl.conf
echo "fs.inotify.max_user_watches=99999999"  >>  /etc/sysctl.conf
echo "fs.inotify.max_user_instances=65535"   >>  /etc/sysctl.conf

cat > /usr/local/sersync/confxml.xml <<eof
<?xml version="1.0" encoding="ISO-8859-1"?>
<head version="2.5">
    <host hostip="localhost" port="8008"></host>
    <debug start="true" />
    <fileSystem xfs="false" />
    <filter start="false">
        <exclude expression="(.*)\.php"></exclude>
        <exclude expression="^data/*"></exclude>
    </filter>
    <inotify>
        <delete start="true" />
        <createFolder start="true" />
        <createFile start="false" />
        <closeWrite start="true" />
        <moveFrom start="true" />
        <moveTo start="true" />
        <attrib start="false" />
        <modify start="false" />
    </inotify>
    <sersync>
        <localpath watch="${agen_watch_dir}">
            <remote ip="${rsync_sevip}" name="${rsync_module}" />
        </localpath>
        <rsync>
            <commonParams params="-artuz" />
            <auth start="true" users="rsync" passwordfile="/usr/local/sersync/user.pass" />
            <userDefinedPort start="false" port="874" />
            <!-- port=874 -->
            <timeout start="false" time="100" />
            <!-- timeout=100 -->
            <ssh start="false" />
        </rsync>
        <failLog path="/tmp/rsync_fail_log.sh" timeToExecute="60" />
        <crontab start="false" schedule="600">
            <crontabfilter start="false">
                <exclude expression="*.php"></exclude>
                <exclude expression="info/*"></exclude>
            </crontabfilter>
        </crontab>
        <plugin start="false" name="command" />
    </sersync>
    <plugin name="command">
        <param prefix="/bin/sh" suffix="" ignoreError="true" />
        <!--prefix /opt/tongbu/mmm.sh suffix-->
        <filter start="false">
            <include expression="(.*)\.php" />
            <include expression="(.*)\.sh" />
        </filter>
    </plugin>
    <plugin name="socket">
        <localpath watch="/home/demo">
            <deshost ip="210.36.158.xxx" port="8009" />
        </localpath>
    </plugin>
    <plugin name="refreshCDN">
        <localpath watch="/data0/htdocs/cdn.markdream.com/site/">
            <cdninfo domainname="cdn.chinacache.com" port="80" username="xxxx" passwd="xxxx" />
            <sendurl base="http://cdn.markdream.com/cms" />
            <regexurl regex="false" match="cdn.markdream.com/site([/a-zA-Z0-9]*).cdn.markdream.com/images" />
        </localpath>
    </plugin>
</head>
eof

	sysctl -p /etc/sysctl.conf
	echo "${agen_rsync_pass:=12345}" > /usr/local/sersync/user.pass
	do="nohup /usr/local/sersync/sersync2 -r -d -n ${t_num:=2} -o /usr/local/sersync/confxml.xml > /usr/local/sersync/rsync.log 2>&1 &"
	echo ${do} >> /etc/rc.local
	eval ${do} && echo -e "\033[32mSersync dameon start ok... \033[0m"
}

read -p "how to config? : S(1) or C(2) help(3) " -t 5 -n 1 var

case $var in  
    	1)  serv_config  					#输入为1时执行服务端设置
    	;;  				
    	2)  agen_config  					#输入为2时执行客户端挂载
	;;
	3)  echo "Serv_List example：  rsync --list-only  <username>@<serverip>::<modulename>"
	;;	
	*)  exit 0
	;;
esac


#----------------------------------------------------------------------------------------------------------------------
#nohup /usr/local/sersync/sersync2 -r -d -o /usr/local/sersync/img.xml > /usr/local/sersync/img.log 2>&1 &

# -d:启用守护进程模式
# -r:在监控前，将监控目录与远程主机用rsync命令推送一遍
# -n: 指定开启守护线程的数量，默认为10个
# -o:指定配置文件，默认使用confxml.xml文件

#双向同步思路:双向同步只需要在把主从配置中的反过来配置一遍就行了,xml配置文件中的配置也为对方ip地址和目录.


#sersync是使用c++编写，而且对linux系统文件系统产生的临时文件和重复的文件操作进行过滤（详细见附录，这个过滤脚本程序没有实现），所以在结合rsync同步的时候，节省了运行时耗和网络资源。因此更快。
#相比较上面两个项目，sersync配置起来很简单，其中bin目录下已经有基本上静态编译的2进制文件，配合bin目录下的xml配置文件直接使用即可。
#另外本项目相比较其他脚本开源项目，使用多线程进行同步，尤其在同步较大文件时，能够保证多个服务器实时保持同步状态。
#本项目有出错处理机制，通过失败队列对出错的文件重新同步，如果仍旧失败，则按设定时长对同步失败的文件重新同步。
#本项目自带crontab功能，只需在xml配置文件中开启，即可按您的要求，隔一段时间整体同步一次。无需再额外配置crontab功能。
#本项目socket与http插件扩展，满足您二次开发的需要。



#环境：
#    前提：gcc automake 那些编译环境要安装好...
#	仅用于Centos6、7系列，其他未测试
#    服务器A（主服务器）
#    服务器B（从服务器/备份服务器）
#    rsync默认TCP端口为873




#修改confxml.conf【这里改成变量】
#vim /usr/local/sersync/confxml.xml
#<?xml version="1.0" encoding="ISO-8859-1"?>
#<head version="2.5">
# <host hostip="localhost" port="8008"></host>		#本机ip和要监听的端口，可不修改
# <debug start="true"/>								#开始debug信息，会在sersync当前运行台，打印Debug信息
# <fileSystem xfs="false"/>							#是否支持xfs文件系统（对于xfs文件系统的用户，需要将这个选项开启，才能使sersync正常工作.）
# <filter start="false">								#是否开始文件过滤，可以在下面添加过滤类型
# <exclude expression="(.*)\.php"></exclude>
# <exclude expression="^data/*"></exclude>
# </filter>   
# <inotify>											#inotify监控的事件
# <delete start="true"/>								#是否保持Sersync和同步端两端文件完全一致
# <createFolder start="true"/> 						#创建目录的支持，如果不开始，不能监控子目录
# <createFile start="false"/>						#是否监控文件的创建
# <closeWrite start="true"/>							#是否监控文件关闭，开始可保证文件的完整性
# <moveFrom start="true"/>
# <moveTo start="true"/>
# <attrib start="false"/>
# <modify start="false"/>
# </inotify>
#
# <sersync>           
# <localpath watch="/home/"> <!-- 本服务器要同步到对端Rsync服务的目录路径--> 			  #替换成变量
# <remote ip="8.8.8.8" name="rsync"/> <!-- 对端Rsync服务的IP和模块名-->                    #替换成变量
# <!--<remote ip="192.168.28.39" name="tongbu"/>--> <!-- 其他的Rync服务的IP和模块名 -->    #替换成变量
# <!--<remote ip="192.168.28.40" name="tongbu"/>--> <!-- 其他的Rync服务的IP和模块名 -->    #替换成变量
# </localpath>
# <rsync>
# <commonParams params="-artuz"/>    #rsync的参数
# <auth start="true" users="rsync" passwordfile="/usr/local/sersync/user.pass"/> <!-- rsync帐号及其密码文件，即对端Rync的认证信息-->
# <userDefinedPort start="false" port="874"/><!-- port=874 -->      #定义rsync端口
# <timeout start="false" time="100"/><!-- timeout=100 -->
# <ssh start="false"/>         #Rsync的时候，是否使用ssh加密
# </rsync>
# <failLog path="/tmp/rsync_fail_log.sh" timeToExecute="60"/><!--default every 60mins execute once--><!-- 修改失败日志记录（可选）-->  #sersync传输失败脚本路径，每隔60分钟重新执行此脚本，执行完毕自动清空
# <crontab start="false" schedule="600"><!--600mins-->     #定义crontab定期完全同步两端文件
# <crontabfilter start="false">    #crontab同步时候的过滤条件，上面的过滤部开头要开
# <exclude expression="*.php"></exclude>
# <exclude expression="info/*"></exclude>
# </crontabfilter>
# </crontab>
# <plugin start="false" name="command"/>
# </sersync>
#
# <!-- 下面这些有关于插件你可以忽略了 -->
# <plugin name="command">
# <param prefix="/bin/sh" suffix="" ignoreError="true"/> <!--prefix /opt/tongbu/mmm.sh suffix-->
# <filter start="false">
# <include expression="(.*)\.php"/>
# <include expression="(.*)\.sh"/>
# </filter>
# </plugin>
#
# <plugin name="socket">
# <localpath watch="/home/demo">
# <deshost ip="210.36.158.xxx" port="8009"/>
# </localpath>
# </plugin>
# <plugin name="refreshCDN">
# <localpath watch="/data0/htdocs/cdn.markdream.com/site/">
# <cdninfo domainname="cdn.chinacache.com" port="80" username="xxxx" passwd="xxxx"/>
# <sendurl base="http://cdn.markdream.com/cms"/>
# <regexurl regex="false" match="cdn.markdream.com/site([/a-zA-Z0-9]*).cdn.markdream.com/images"/>
# </localpath>
# </plugin>
#</head>


#要 Kill rsync 进程，不要用 kill -HUP {PID} 的方式重启进程，以下3种方式任选
#ps -ef|grep rsync|grep -v grep|awk '{print $2}'|xargs kill -9
#cat /var/run/rsyncd.pid | xargs kill -9 【写到脚本选项里】
#pkill rsync

