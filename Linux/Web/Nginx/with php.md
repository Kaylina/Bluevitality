>**前提：Centos6. 64位纯净版系统，最好有安装了Mysql数据库，没有安装也没有所谓，只是基础篇。**

## 安装编译环境篇
	yum clean all && \
	        yum -y install gcc* \
	        make autoconf libtool-ltdl-devel gd-devel \
	        freetype* libxml2-devel libjpeg-devel \
	        libpng-devel openssl-devel \
	        curl-devel patch libmcrypt-devel \
	        libmhash-devel ncurses-devel bzip2 \
	        libcap-devel ntp sysklogd \
	        diffutils sendmail unzip \
	        bison wget tar re2c
 

## 安装libiconv库篇
#### step1：下载软件

	wget http://ftp.gnu.org/pub/gnu/libiconv/libiconv-1.9.2.tar.gz

>注意：如果没有这个库，在编译php时会提示报错而停止编译安装，libiconv属于动态库

#### step2：编译安装
	tar xf libiconv-1.14.tar.gz -C /usr/src/
	cd /usr/src/libiconv-1.9.2
	./configure --prefix=/usr/local/libiconv
	make && make install
 

## 安装PHP5.3篇
#### step1：设置运行用户
	useradd -M -s /sbin/nologin www

>注意：创建一个不需要家目录，不需要登录系统的运行用户，它只能是支持php和nginx运行在Linux上，每一个用户的权限必须细分，否则后期很麻烦。


#### step2：下载php
	wget http://museum.php.net/php5/php-5.3.10.tar.gz
 

>注意：文章开始的下载时windows下载方式，而这个是linux下载方式，软件都是一样
 

#### step3：配置编译安装PHP
	tar xf php-5.3.10.tar.gz -C /usr/src/
	./configure \
	 --prefix=/usr/local/php \
	 --with-config-file-path=/usr/local/php/ \
	 --with-mysql=mysqlnd \
	 --with-gd --with-jpeg-dir \
	 --enable-pdo --with-pdo-mysql \
	 --enable-mbstring --with-mysqli \
	 --with-png-dir --with-freetype-dir \
	 --enable-gd-native-ttf \
	 --with-mcrypt --with-curl \
	 --enable-fpm \
	 --with-gettext --disable-debug \
	 --enable-zend-multibyte \
	 --with-mhash --disable-ipv6 \
	 --with-iconv=/usr/local/libiconv \
	 --with-mcrypt && \
	make && make install
 

#### 一些参数介绍：

	prefix：php安装目录路径
	
	with-config-file-path：php.ini主配置文件存放位置，注意编译安装php.ini文件是不存在的，需要手动创建放在这个目录下
	
	with-mysql：启用mysql
	
	with-libxml-dir：指定libxml库目录，不指定时使用默认目录/usr/lib64下
	
	enable-ftp：支持FTP，然而好像并没有什么用。
	
	enable-sockets：支持sockets扩展，后期安装邮件服务时会使用这个扩展
	
	with-gd：支持GD库，很重要的一个扩展
	
	with-jpeg-dir：使GD支持jpeg图片格式
	
	with-png-dir：使GD支持png图片格式
	
	with-freetype-dir：使GD支持其他格式图片
	
	with-zlib-dir：使nginx支持zlib扩展
	
	enable-gd-native-ttf：启用TureType字符功能
	
	enable-magic-quotes：默认激活magic quotes。可让程序在执行时自动加入反斜线的引入字符
	
	with-iconv：启用XMLRPC-EPI：iconv支持
	
	enable-mbstring=all：启用多字节字符串的支持
	
	disable-cgi：编译禁用CGI的PHP版本，cgi版本已经慢慢淘汰了，由fastcgi代替
	
	with-openssl：支持SSL协议
	
	with-mcrypt：包含mcrypt支持
	
	enable-bcmath：启用bcmatch（公元前风格精度数学）
	
	enable-calendar：启用日历转换支持
	
	enable-exif：启用EXIF支持（从图片中获取元数据）
	
	enable-libxml：启用LIBXML支持
	
	with-bz2：包含BZip2支持
	
	with-curl：启用cURL支持
	
	with-xmlrpc：包含XMLRPC-EPI支持
	
	with-gettext：包含GNU gettext支持
	
	disable-cli：编译禁用CLI的PHP版本
	
	disable-debug：禁止带调试符号的编译
	
	enable-zend-multibyte：编译zend多字节支持
	
	with-mhash：包含mhash支持
	
	enable-pcntl： 启用pcntl支持
	
	enable-sysvsem：启用系统V信号支持
	
	enable-inline-optimization：编译zend_execute.lo需要
	
	注意：如果编译失败，disable-inline-optimization使用这个参数
	
	enable-soap：启用SOAP支持
	
	disable-ipv6：禁止ipv6支持
	
	enable-fpm：启用fpm功能，为nginx整合使用
	
	with-iconv：启用XMLRPC-EPI：iconv支持

 

#### step4：php优化与配置(注意：以下操作在/usr/local/php5/目录下)
	cd /usr/local/php5/
	cp /usr/src/php-5.3.10/php.ini-production  lib/php.ini
	cp etc/php-fpm.conf.default etc/php-fpm.conf
	vim etc/php-fpm.conf
	user = www
	group = www
	pm.max_children = 50
	pm.min_spare_servers = 5
	pm.max_spare_servers = 35
	pm.max_requests = 500
	env[HOSTNAME] = $HOSTNAME
	env[PATH] = /usr/local/bin:/usr/bin:/bin
	env[TMP] = /tmp
	env[TMPDIR] = /tmp
	env[TEMP] = /tmp
 

>注意：php.ini放到/usr/local/php5/lib/目录下才能生效，如果需要在php根目录下，在编译时定义with-config-file-path选项

 

#### 一些参数介绍：

	pm.max_children：子进程最大数
	pm.min_spare_servers：启动时的进程数
	pm.max_spare_servers：保证空闲进程数最小值，如果空闲进程小于此值，则创建新的子进程
	pm.max_requests：保证空闲进程数最大值，如果空闲进程大于此值，此进行清理

#### step5：启动php和停止php服务
	ln -sf /usr/local/php5/sbin/php-fpm /usr/bin/
	php-fpm   #启动php进程
 
>注意：php的默认端口为9000，所以在防火墙上需要添加下9000端口

 

#### 停止php

	pkill php-fpm
 

 

## 小技巧：

#### 如果安装网站时提示不支持某些扩展怎么办？例如不支持mysqli扩展

#### 解决：重编译php，增加扩展模块即可


#### step1：生成新编译文件 (注意：在php解压目录下操作编译/usr/src/php-5.3.10/)

	cd /usr/src/php-5.3.10/ext/mysqli/
 

>注意：php5.3版本tar包中一些常用的扩展模块默认是存在的，需要时可以编译安装


	/usr/local/php5/bin/phpize

>注意：这个很重要，在没有存在aspx编译模块下，phpize也会生成configure文件

	./configure --prefix=/usr/local/php5/include/php/ext/mysqli \
	--with-php-config=/usr/local/php5/bin/php-config \
	--with-mysqli=/usr/local/mysql/bin/mysql_config
 

>注意：添加模块不需要安装，只要配置生成就行了。

 

#### 一些参数介绍：

	prefix：指定模块的安装路径，注意的是编译安装的PHP中在根目录下是没有ext目录，而模块默认存放目录是在/usr/local/php5/include/php/ext/下
	
	with-php-config：指定PHP安装配置信息
	
	with-mysqli：指定Mysql安装配置信息

#### step2：修改php.ini文件

	vim lib/php.ini
	extension=mysqli.so
 

>注意：在php.ini目录直接启用mysqli扩展就行了，而不需要指定mysqli的安装目录，因为在编译时已经把mysqli模块生成到默认的模块存放目录了

#### step3：重启php
	pkill php-fpm ; php-fpm
 

>即可重新加载模块

###### 这个是php添加扩展模块的方法，以后需要添加新模块都可以通过这个方法解决。

 

## 安装Zend篇
#### step1：下载软件

	wget http://liquidtelecom.dl.sourceforge.net/project/wdcp/wdcp_soft/ZendGuardLoader-php-5.3-linux-glibc23-x86_64.tar.gz
 

>注意：如果需要其他版本 eycode带你跳转

#### step2：配置zend
	tar xf ZendGuardLoader-php-5.3-linux-glibc23-x86_64.tar.gz
	cd ZendGuardLoader-php-5.3-linux-glibc23-x86_64/php-5.3.x/
	mkdir /usr/local/php5/include/php/ext/zend
	cp ZendGuardLoader.so /usr/local/php5/include/php/ext/zend/
	
	vim /usr/local/php5/lib/php.ini
	[zend]
	zend_extension = /usr/local/php5/include/php/ext/zend/ZendGuardLoader.so
	zend_loader.enable = 1
	zend_loader.disable_licensing = 0
	zend_loader.obfuscation_level_support = 3
 

>注意：建议使用绝对路径

 

#### 一些参数介绍：

	zend_extension：模块存储目录
	
	zend_loader.enable：启用加载

#### step3：重载php

	pkill php-fpm ; php-fpm

>即可重新加载模块

 

## 安装pcre篇
#### step1：下载pcre

	wget ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-7.7.tar.gz
 

>注意：pcre库是安装nginx的必须环境

#### step2：编译安装

	tar zxvf pcre-7.7.tar.gz -C /usr/src/pcre-7.7
	./configure
	make && make install
 

## 安装Nginx篇
#### step1：下载nginx

	wget  http://nginx.org/download/nginx-1.9.9.tar.gz
 
>注意：1.9.9版本是最新的版本，需要的 eycode带你跳转

#### step2：安装nginx

	tar xf nginx-1.9.9.tar.gz -C /usr/src/
	cd /usr/src/nginx-1.9.9
	./configure --prefix=/usr/local/nginx \
	--with-http_stub_status_module \
	--with-http_gzip_static_module
	make && make install
 

>注意：nginx虽然使用很少的编译参数，但自带的默认参数满足使用


#### 一下参数介绍：

	prefix：指定nginx安装目录
	
	with-http_stub_status_module：监控 Nginx 的当前状态
	
	with-http_gzip_static_module：启动预压缩功能,对所有类型的文件都有效

 

#### step3：配置nginx.conf文件

	vim /usr/local/nginx/conf/nginx.conf
	user www;
	worker_processes 4;
	location / {
	root html;
	index index.html index.htm index.php;
	}
	location ~ \.php$ {
	  root html;
	  fastcgi_pass 127.0.0.1:9000;
	  fastcgi_index index.php;
	  fastcgi_param SCRIPT_FILENAME /scripts$fastcgi_script_name;
	  include fastcgi.conf;
	# include fastcgi_params;
	}
	location ~* \.(gif|jpg|jpeg|png|bmp|swf|htm|html|css|js)$ {
	  root /eycode;
	}
 

#### 一些参数介绍：

	user：运行用户，建议以php的一致，方便管理
	
	worker_processes：进程数，建议与服务器的CPU核数一致即可
	
	root：网站数据存放目录
	
	index：指定默认主页
	
	include：调用外部配置文件

>注意：其他参数在本文中不介绍，因为nginx实在太多东西要学了，文章有限。nginx在后面会有相关专题介绍

#### step4：启动nginx和停止nginx
**启动nginx**
	cd /usr/local/nginx/
	./sbin/nginx

**停止nginx**
	pkill nginx

 
**为了方便管理nginx服务，在网上找了一个管理脚本**


	vim /etc/init.d/nginxd
	
	#!/bin/bash
	# chkconfig: 345 99 20
	# description: Nginx servicecontrol script
	PROG="/usr/local/nginx/sbin/nginx"
	PIDF="/usr/local/nginx/logs/nginx.pid"
	case "$1" in
	start)
	$PROG
	echo "Nginx servicestart success."
	;;
	stop)
	kill -s QUIT $(cat $PIDF)
	echo "Nginx service stopsuccess."
	;;
	restart)
	$0 stop
	$0 start
	;;
	reload)
	kill -s HUP $(cat $PIDF)
	echo"reload Nginx configsuccess."
	;;
	*)
	echo "Usage: $0{start|stop|restart|reload}"
	exit 1
	esac

保存


#### 启动nginx服务

	service nginxd start
 

>注意：如果报错

	error while loading shared libraries: libpcre.so.1: cannot open shared object file:
	No such file or directory
 

#### 解决方案：

	ln -s /usr/local/lib/libpcre.so.1 /lib64
 

#### 重载nginx配置

	service nginxd reload
 

#### 重启nginx服务

	service nginxd restart
 

#### 停止nginx服务

	service nginxd stop
 

 

**OK，nginx和PHP整合终于写完了，写了两个钟的文章，睡一觉去…..88。**
