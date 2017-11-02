>前提：Centos6.* 64位纯净版系统和jsp网站源码用于测试

>注意：虽然是rest风格分离，但本文不会演示，因为这个是网站程序员的事。

 

## 编译环境篇
#### step1：更新yum

	[root@localhost ~]# yum clean all
	[root@localhost ~]# yum makecache
 

#### step2：安装编译环境

	[root@localhost ~]# yum -y install gcc* gcc-c++* \
	autoconf* automake* \
	zlib* libxml* \
	ncurses-devel* libgcrypt* \
	libtool*
 

## 安装Pcre库篇
#### step1：下载Pcre源码包

	[root@localhost ~]# wget http://nchc.dl.sourceforge.net/project/pcre/pcre/7.7/pcre-7.7.tar.gz
 

>注意：如果需要其他版本的Pcre 点击eycode跳转

 

#### step2：编译安装

	[root@localhost ~]# tar xf pcre-7.7.tar.gz -C /usr/src/
	[root@localhost ~]# cd /usr/src/pcre-7.7/
	[root@localhost pcre-7.7]# ./configure && make && make install
	 

>注意：Pcre库是Nginx安装必备库，nginx的编译很多是依赖这个库文件

 

## 安装Nginx篇
#### step1：下载Nginx版本

	[root@localhost ~]# wget http://nginx.org/download/nginx-1.9.9.tar.gz
 

>注意：nginx1.9是最新版本，如果需要 eycode带你跳转

 

#### step2：安装Nginx

	[root@localhost ~]# tar xf nginx-1.9.9.tar.gz -C /usr/src/
	[root@localhost ~]# cd /usr/src/nginx-1.9.9/
	[root@localhost nginx-1.9.9]# ./configure --prefix=/usr/local/nginx \
	--with-http_stub_status_module \
	--with-http_gzip_static_module
	[root@localhost nginx-1.9.9]# make && make install

#### step3：配置Nginx.conf文件 (注意：以下规则都是在http{}模块下编写或添加)

	[root@localhost nginx]# useradd -M -s /sbin/nologin www
	[root@localhost nginx-1.9.9]# cd /usr/local/nginx/
	[root@localhost nginx]# vim conf/nginx.conf
	user www;
	worker_processes 2;
	error_log logs/error.log;
	worker_rlimit_nofile 5120;
	#pid logs/nginx.pid;
	events {
	 use epoll;
	 worker_connections 5120;
	}
	
	http {
	 include mime.types;
	 default_type application/octet-stream;
	
	 log_format main '$remote_addr - $remote_user [$time_local] "$request" '
	 '$status $body_bytes_sent "$http_referer" '
	 '"$http_user_agent" "$http_x_forwarded_for"';
	
	 access_log logs/access.log main;
	
	 sendfile on;
	 #tcp_nopush on;
	 tcp_nodelay on;
	
	 #keepalive_timeout 0;
	 keepalive_timeout 65;
	
	 gzip on;
	 gzip_http_version 1.0;
	 gzip_disable "MSIE[1-6]";
	 gzip_types text/plain application/x-javascript text/css text/javascript application/x-httpd-php;
	 gzip_proxied any;
	 gzip_min_length 1024;
	 gzip_buffers 4 8k;
	 gzip_comp_level 5;
	
	 include vhost/*.conf;
	
	}

#### 一些参数：

	user www; 									#指定运行用户
	worker_processes 3; 						#进程数，建议与CPU核数一致
	
	#在http{}模块中定义
	
	gzip on;                                    #启用gzip压缩
	gzip_http_version 1.0;          			#代理使用http1.0版本进行gzip
	gzip_disable “MSIE [1-6].”; 					#禁止IE1~6进行压缩
	gzip_types text/plain application/x-javascript text/css text/javascript application/x-httpd-php;
												#定义压缩文件类型
	gzip_proxied any;                 			#凡是代理的全部压缩
	gzip_min_length 1024;       				#最小长度
	gzip_buffers 4 8k;                			#压缩缓存
	gzip_comp_level 3;             				#压缩率1最小，9最大
	include vhost/*.conf;          				#设置虚拟主机

 

#### step4：创建虚拟主机

	[root@localhost nginx]# mkdir conf/vhost
	[root@localhost nginx]# vim conf/vhost/test.conf
	    server {
	        listen       80;
	        server_name  eycode.com www.eycode.com;
	        location  / {
	                index           index.jsp;
	                proxy_pass      http://127.0.0.1:8080;
	                proxy_redirect  off;
	                proxy_set_header        Host $host;
	                proxy_set_header        X-Real-IP $remote_addr;
	                proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
	                client_max_body_size    10m;
	                client_body_buffer_size 128k;
	                proxy_connect_timeout   90;
	                proxy_read_timeout      90;
	                proxy_buffer_size       4k;
	                proxy_buffers           6 32k;
	                proxy_busy_buffers_size 64k;
	                proxy_temp_file_write_size 64k;
	        }
	        location ~* \.(gif|jpg|png|bmp|swf|txt)$ {
	                root /web;
	                expires 30d;
	        }
	        location ~* \.(js|css|html|htm)$ {
	                root /web;
	                expires 1d;
	        }
		}
	 

#### 一些参数：

	listen 80;                              			#监听80端口
	server_name eycode.com www.eycode.com; 				#绑定域名
	
#### 由tomcat处理动态页面
	index index.jsp;                                    #默认主页
	proxy_pass http://127.0.0.1:8080;          			#不需要指定网站的根目录，凡是请求都给tomcat处理
	proxy_redirect off;                                 #对发送给客户端的URL进行修改
	proxy_set_header Host $host;                  		#后端的Web服务器可以通过X-Forwarded-For获取用户真实IP
	proxy_set_header X-Real-IP $remote_addr;
	proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
	client_max_body_size 10m;                     		#允许客户端请求的最大单文件字节数
	client_body_buffer_size 128k;                 		#缓冲区代理缓冲用户端请求的最大字节数
	proxy_connect_timeout 90;                     		#nginx跟后端服务器连接超时时间
	proxy_read_timeout 90;                          	#连接成功后，后端服务器响应时间
	proxy_buffer_size 4k;                               #设置代理服务器,保存用户头信息的缓冲区大小
	proxy_buffers 6 32k;                                #proxy_buffers缓冲区，网页平均在32k以下的话
	proxy_busy_buffers_size 64k;                		#高负荷下缓冲大小=proxy_buffers*2
	proxy_temp_file_write_size 64k;          			#设定缓存文件夹大小，大于这个值,将从upstream服务器
#### 由nginx处理静态页面
	location ~* \.(gif|jpg|png|bmp|swf)$ {   			#定义nginx应该处理哪些文件
	root /web;                                          #指定网站根目录
	expires 30d;                                        #保留时间
	}
	location ~* \.(js|css|html|htm)$ {
	root /web;
	expires 1d;
	}

 

#### step5：启动Nginx服务

	[root@localhost nginx]# pkill nginx ; ./sbin/nginx
	[root@localhost nginx]#
	[root@localhost nginx]# netstat -anput |grep nginx
	tcp 0 0 0.0.0.0:80 0.0.0.0:* LISTEN 63171/nginx
	[root@localhost nginx]#
 

>注意：建议使用Nginx的管理脚本，nginx管理脚本教程

 

## 安装JDK环境篇
#### step1：下载新版的JDK

	[root@localhost ~]# wget -O jdk-8u65-linux-x64.tar.gz http://download.oracle.com/otn-pub/java/jdk/8u65-b17/jdk-8u65-linux-x64.tar.gz?AuthParam=1451909486_9eaa773a548bf32f31b69a39945ae580
>注意：上面下载不了，请 点击JDK下载

 

#### step2：配置java环境

	[root@localhost ~]# tar xf jdk-8u45-linux-x64.tar.gz -C /usr/src/
	[root@localhost ~]# mkdir /usr/local/jdk
	[root@localhost ~]# cp -a /usr/src/jdk1.8.0_45/* /usr/local/jdk/
	[root@localhost ~]# ln -sf /usr/local/jdk/bin/java /usr/bin/
	[root@localhost ~]# ln -sf /usr/local/jdk/bin/javac /usr/bin/
	
	[root@localhost ~]# cat /etc/profile
	JAVA_HOME=/usr/local/jdk
	CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar:$CATALINA_HOME/lib/servlet-api.jar
	PATH=$JAVA_HOME/bin:$PATH
	export JAVA_HOME CACTALINA_HOME CLASSPATH PATH
	
	[root@localhost ~]# source /etc/profile
	[root@localhost ~]# java -version
	java version "1.8.0_45"
	Java(TM) SE Runtime Environment (build 1.8.0_45-b14)
	Java HotSpot(TM) 64-Bit Server VM (build 25.45-b02, mixed mode)
	[root@localhost ~]#
 

## 安装Tomcat篇
#### step1：下载tomcat

	[root@localhost ~]# wget http://mirrors.cnnic.cn/apache/tomcat/tomcat-8/v8.0.30/bin/apache-tomcat-8.0.30.tar.gz
 

>注意：tomcat8.0是最新版本

 

#### step2：创建启动和停止脚本

	[root@localhost ~]# mkdir /usr/local/tomcat
	[root@localhost ~]# cp -ap /usr/src/apache-tomcat-8.0.30/* /usr/local/tomcat/
	[root@localhost ~]# ln -sf /usr/local/tomcat/bin/startup.sh /usr/bin/tomcat-up
	[root@localhost ~]# ln -sf /usr/local/tomcat/bin/shutdown.sh /usr/bin/tomcat-down

#### step3：修改配置文件

#### 修改前

	<Host name="localhost"  appBase="webapps"  unpackWARs="true" autoDeploy="true">

#### 修改后 (自定义网站根目录)
	<Host name="localhost" appBase="webapps" unpackWARs="true" autoDeploy="true">
	<Context path="" docBase="/web" debug="0"/>
>注意：docBase指定网站根目录。

 

#### step4：启动tomcat服务

	[root@localhost tomcat]# mkdir /web
	[root@localhost tomcat]# tomcat-up
	Using CATALINA_BASE: /usr/local/tomcat
	Using CATALINA_HOME: /usr/local/tomcat
	Using CATALINA_TMPDIR: /usr/local/tomcat/temp
	Using JRE_HOME: /usr
	Using CLASSPATH: /usr/local/tomcat/bin/bootstrap.jar:/usr/local/tomcat/bin/tomcat-juli.jar
	Tomcat started.
	[root@localhost tomcat]#
	[root@localhost tomcat]# netstat -anput |grep java
	tcp 0 0 :::8080 :::* LISTEN 63562/java
	tcp 0 0 :::8009 :::* LISTEN 63562/java
	[root@localhost tomcat]#

>注意：如果自定义了网站根目录，必须该目录是存在的，如果不存在tomcat是无法启动正常的。

 
## 测试篇
>注意：测试很简单，不需要创建文件，测试不存在的页面文件即可知道

>思路：提交html页面是否是nginx处理，提交jsp页面是否是tomcat处理

 

#### step1：测试html静态页面

	[root@localhost ~]# curl http://www.eycode.com/test.html
	<html>
	<head><title>404 Not Found</title></head>
	<body bgcolor="white">
	<center><h1>404 Not Found</h1></center>
	<hr><center>nginx/1.9.9</center>
	</body>
	</html>
 
>注意：根据报错显示，404页面不存在，是由nginx处理。

 

#### tep2：测试jsp动态页面

	[root@localhost ~]# curl http://www.eycode.com/test.jsp
	<!DOCTYPE html>
	<html>
	<head>
	<title>Apache Tomcat/8.0.30 - Error report</title>
	</head>
	</html>
	[root@localhost ~]#
 
>注意：根据报错提示，jsp页面是提交给tomcat处理。


**总结：根据文章开头说的rest请求分离，就是把rest请求提交给tomcat处理，其他的静态页面让Nginx自身处理
所以如果处理好动静分离，这个问题就很容易解决。**
