
>前提：Centos6.*  64位/纯净版系统


## 预安装环境篇

#### step1：更新yum
	[root@ZWN2K-5001 ~]# yum clean all
	[root@ZWN2K-5001 ~]# yum makecache

>注意：清除Yum库缓存，更新缓存

 

#### step2：安装编译环境
	[root@ZWN2K-5001 ~]# yum -y install gcc gcc-c++ \
	libxml2 libxml2-devel \
	zlib-devel \
	curl curl-devel \
	libjpeg-devel libjpeg \
	libpng-devel freetype-devel

 

## 安装Apache篇

#### step1：下载软件
	[root@ZWN2K-5001 ~]# wget http://archive.apache.org/dist/httpd/httpd-2.2.12.tar.gz
>注意：如果需要其他版本  点击eycode跳转

 

#### step2：编译安装
	[root@ZWN2K-5001 ~]# tar xf httpd-2.2.12.tar.gz -C /usr/src/
	[root@ZWN2K-5001 ~]# cd /usr/src/httpd-2.2.12/
	[root@ZWN2K-5001 httpd-2.2.12]#
	[root@ZWN2K-5001 httpd-2.2.12]# ./configure \
	--prefix=/usr/local/http \
	--enable-vhost-alias \
	--enable-rewrite \
	--enable-so \
	--enable-charset-lite \
	--enable-cgi
	[root@ZWN2K-5001 httpd-2.2.12]# make && make install

 

### 一些参数

	prefix：安装路径
	
	enable-vhost-alias：禁用内容协商
	
	enable-rewrite：启用重定向
	
	enable-so： 启用动态加载模块支持
	
	enable-charset-lite： 启动字符集支持
	
	enable-cgi： 启用 CGI 脚本程序支持

>注意： 如果要网站的扩展功能，一定要在配置时启用 “–enable-so “和” enable -cgi “支持

 

#### step3：优化路径
	[root@ZWN2K-5001 httpd-2.2.12]# ln -sf /usr/local/http/bin/* /usr/local/bin/
	[root@ZWN2K-5001 httpd-2.2.12]# httpd -v
	Server version: Apache/2.2.12 (Unix)
	Server built: Jan 5 2016 18:56:25
	[root@ZWN2K-5001 httpd-2.2.12]#
	[root@ZWN2K-5001 httpd-2.2.12]# cp /usr/local/http/bin/apachectl /etc/init.d/httpd
	[root@ZWN2K-5001 httpd-2.2.12]#
	[root@ZWN2K-5001 httpd-2.2.12]# vim /etc/init.d/httpd
	[root@ZWN2K-5001 httpd-2.2.12]#
	[root@ZWN2K-5001 httpd-2.2.12]# head /etc/init.d/httpd
	#!/bin/sh
	# chkconfig:35 85 15
	# description: It is httpd server
	# Licensed to the Apache Software Foundation (ASF) under one or more
	[root@ZWN2K-5001 httpd-2.2.12]# chkconfig --add httpd
	[root@ZWN2K-5001 httpd-2.2.12]# chkconfig --list httpd
	httpd 0:关闭 1:关闭 2:关闭 3:启用 4:关闭 5:启用 6:关闭
	[root@ZWN2K-5001 httpd-2.2.12]#

 

#### 一些参数：

	chkconfig:35 85 15                     	：服务识别参数，级别 3， 5 中启动
	description: It is httpd server  		：服务的描述信息 (自定义内容)

>注意：如果没有创建软链接的，是不能够使用快捷方式查看的

 

## 安装libmcrypt篇

#### step1：下载软件
	[root@ZWN2K-5001 ~]# wget http://nchc.dl.sourceforge.net/project/mcrypt/Libmcrypt/2.5.8/libmcrypt-2.5.8.tar.gz

 

#### step2：编译安装
	[root@ZWN2K-5001 ~]# tar xf libmcrypt-2.5.8.tar.gz -C /usr/src/
	[root@ZWN2K-5001 ~]# cd /usr/src/libmcrypt-2.5.8/
	[root@ZWN2K-5001 libmcrypt-2.5.8]# ./configure && make && make install
	[root@ZWN2K-5001 libmcrypt-2.5.8]# ln -sf /usr/local/lib/libmcrypt.* /usr/lib/

 

## 安装mhash篇

#### step1：下载软件
	[root@ZWN2K-5001 ~]# wget http://nchc.dl.sourceforge.net/project/mhash/mhash/0.9.9.9/mhash-0.9.9.9.tar.gz

 

#### step2：编译安装
	[root@ZWN2K-5001 mhash-0.9.9.9]# tar xf mhash-0.9.9.9.tar.gz -C /usr/src/
	[root@ZWN2K-5001 mhash-0.9.9.9]# cd /usr/src/mhash-0.9.9.9/
	[root@ZWN2K-5001 mhash-0.9.9.9]# ./configure && make && make install
	[root@ZWN2K-5001 mhash-0.9.9.9]# ln -sf /usr/local/lib/libmhash.* /usr/lib/

 

## 安装mcrypt篇

#### step1：下载软件
	[root@ZWN2K-5001 ~]# wget http://nchc.dl.sourceforge.net/project/mcrypt/MCrypt/2.6.8/mcrypt-2.6.8.tar.gz

 

#### step2：编译安装
	[root@ZWN2K-5001 ~]# tar xf mcrypt-2.6.8.tar.gz -C /usr/src/
	[root@ZWN2K-5001 ~]# cd /usr/src/mcrypt-2.6.8/
	[root@ZWN2K-5001 mcrypt-2.6.8]# LD_LIBRARY_PATH=/usr/local/lib ./configure && make && make install


>注意：LD_LIBRARY_PATH指定动态链接库目录，如果没有mcrypt编译失败

 

## 安装libiconv篇

#### step1：下载软件
	[root@ZWN2K-5001 ~]# wget http://ftp.gnu.org/pub/gnu/libiconv/libiconv-1.9.2.tar.gz

 

#### step2：编译安装
	[root@ZWN2K-5001 ~]# tar xf libiconv-1.9.2.tar.gz -C /usr/src/
	[root@ZWN2K-5001 ~]# cd /usr/src/libiconv-1.9.2/
	[root@ZWN2K-5001 libiconv-1.9.2]# ./configure --prefix=/usr/local/libiconv
	[root@ZWN2K-5001 libiconv-1.9.2]# make && make install

 

##安装PHP篇

#### step1：下载软件
	[root@ZWN2K-5001 ~]# wget http://museum.php.net/php5/php-5.3.10.tar.gz

 

#### step2：编译安装

 
	[root@ZWN2K-5296 ~]# tar xf php-5.3.10.tar.gz -C /usr/src/
	[root@ZWN2K-5296 ~]# cd /usr/src/php-5.3.10/
	[root@ZWN2K-5001 php-5.3.10]# ./configure \
	--prefix=/usr/local/php \
	--with-apxs2=/usr/local/http/bin/apxs \
	--with-config-file-path=/usr/local/php/ \
	--with-mysql=mysqlnd \
	--with-gd --with-jpeg-dir \
	--enable-pdo --with-pdo-mysql  \
	--enable-mbstring --with-mysqli \
	--with-png-dir --with-freetype-dir \
	--enable-gd-native-ttf \
	--with-mcrypt --with-curl \
	--with-gettext --disable-debug \
	--enable-zend-multibyte \
	--with-mhash --disable-ipv6 \
	--with-iconv=/usr/local/libiconv \
	--with-mcrypt
	[root@ZWN2K-5001 php-5.3.10]# make && make install

 

>注意：参数详细请 点击eycode跳转

 

#### step3：生成配置文件
	[root@ZWN2K-5001 php-5.3.10]# cp php.ini-production /usr/local/php/php.ini

 

>注意：php配置样例文件有两个，eycode建议使用production生产环境配置文件

 

## 安装Zend篇

##### step1：下载软件
	[root@ZWN2K-5001 ~]# wget http://liquidtelecom.dl.sourceforge.net/project/wdcp/wdcp_soft/ZendGuardLoader-php-5.3-linux-glibc23-x86_64.tar.gz

 

#### step2：修改php配置文件
	[root@ZWN2K-5001 ~]# mkdir /usr/local/php/include/php/ext/zend
	[root@ZWN2K-5001 ~]# tar xf ZendGuardLoader-php-5.3-linux-glibc23-x86_64.tar.gz -C /usr/src/
	[root@ZWN2K-5001 ~]# cd /usr/src/ZendGuardLoader-php-5.3-linux-glibc23-x86_64/php-5.3.x/
	[root@ZWN2K-5001 php-5.3.x]# cp * /usr/local/php/include/php/ext/zend/
	[root@ZWN2K-5001 php-5.3.x]#
	[root@ZWN2K-5001 php-5.3.x]# vim /usr/local/php/php.ini
	[zend]
	zend_extension = /usr/local/php/include/php/ext/zend/ZendGuardLoader.so
	zend_loader.enable = 1
	zend_loader.disable_licensing = 0
	zend_loader.obfuscation_level_support = 3

 

## 配置apache主配置文件篇

#### step1：修改配置文件
	[root@ZWN2K-5001 ~]# cd /usr/local/http/
	[root@ZWN2K-5001 http]# vim conf/httpd.conf
	Listen 127.0.0.1:80
	LoadModule php5_module modules/libphp5.so
	AddType application/x-httpd-php    .php
	DirectoryIndex index.php

 

>注意：
>
1.	部分网站必须使用80端口，而读者自意识认为一个端口不能使用相同的服务，但是在Linux系统下不要忘记有本地环回地址和外网地址，只要绑定不同地址就可以共用了。
2.	LoadModule php5_module modules/libphp5.so这个参数在编译完php后会自动写入，如果没有写入可能是php没有编译成功。
3.	AddType application/x-httpd-php识别符，允许运行php脚本文件，需要手动添加
4.	DirectoryIndex首页默认文件，写一个index.php就行了，html/htm等文件都交给了nginx处理。

 

#### step2：启动http服务
	[root@ZWN2K-5001 http]# service httpd start
	httpd (pid 11360) already running
	[root@ZWN2K-5001 http]#
	[root@ZWN2K-5001 http]# netstat -anput |grep 80
	tcp 0 0 127.0.0.1:80 0.0.0.0:* LISTEN 11360/httpd

 

>注意：如果没有软连接到/etc/init.d/目录下，是不能是使用service命令管理的。

 

## 安装eAccelerator  PHP加速器篇

#### step1：下载软件
	[root@ZWN2K-5001 ~]# wget https://github.com/eaccelerator/eaccelerator/tarball/master

 

>注意：下载到这个文件，请不要惊讶，是对的，也不需要 “-O” 参数

 

#### step2：编译安装
	[root@ZWN2K-5001 ~]# tar xf master -C /usr/src/
	[root@ZWN2K-5001 ~]# cd /usr/src/eaccelerator-eaccelerator-42067ac/
	[root@ZWN2K-5001 eaccelerator-eaccelerator-42067ac]# /usr/local/php/bin/phpize
	Configuring for:
	PHP Api Version: 20090626
	Zend Module Api No: 20090626
	Zend Extension Api No: 220090626

 

>注意：phpize是用来扩展php扩展模块的，通过phpize可以建立php的外挂模块，生成一个configure脚本，值得留意的是php编译好后会把phpize放到php安装目录下的bin目录中。

 
	[root@ZWN2K-5001 eaccelerator-eaccelerator-42067ac]# ./configure --enable-eaccelerator=shared --with-php-config=/usr/local/php/bin/php-config
	[root@ZWN2K-5001 eaccelerator-eaccelerator-42067ac]# make && make install
	Installing shared extensions: /usr/local/php/lib/php/extensions/no-debug-non-zts-20090626/
	+-------------------------------------------------------+
	| !!! Attention !!! |
	| |
	| For disk cache users (using eaccelerator.shm_only=0): |
	| |
	| Please remember to empty your eAccelerator disk cache |
	| when upgrading, otherwise things will break! |
	+-------------------------------------------------------+

 

>注意：
>
1.	php-config这个文件中保存了php所有的配置信息，添加扩展时会自动获取到php的配置信息
2.	/usr/local/php/lib/php/extensions/no-debug-non-zts-20090626/这个地址是编译后模块存放地址，让php加载

 

#### step3：修改php配置文件
	[root@ZWN2K-5001 ~]# vim /usr/local/php/php.ini
	[eaccelerator]
	extension="/usr/local/php/lib/php/extensions/no-debug-non-zts-20090626/eaccelerator.so"
	eaccelerator.shm_size="64"
	eaccelerator.cache_dir="/tmp/eaccelerator"
	eaccelerator.enable="1"
	eaccelerator.optimizer="1"
	eaccelerator.check_mtime="1"
	eaccelerator.debug="0"
	eaccelerator.filter=""
	eaccelerator.shm_max="0"
	eaccelerator.shm_ttl="0"
	eaccelerator.shm_only="0"
	eaccelerator.compress="1"
	eaccelerator.compress_level="9"

 

#### 一些参数：
>
1. extension：加载eaccelerator模块
2. eaccelerator.shm_size：用来设置分配给eAccelerator用来缓存php的最大共享内存，单位是mb，如果设置为0，就使用默认大小。
3. eaccelerator.cache_dir：用来设置硬盘缓存目录。eA用来存放预编译代码，session数据，内容和用户入口。默认值是”/tmp/eaccelerator”
4. eaccelerator.enable：用来设置是否启用或禁用eAccelerator，设置1为启用，设置0为禁用
5. eaccelerator.optimizer：开启或关闭优化，用户加速代码的执行。1为开启，0为关闭，优化仅仅在脚本被编译时候发生并且是在被缓存之前
6. eaccelerator.check_mtime：在每次命中的时候Eaccelerator都会检查脚本的修改时间来判断是不是脚本发生的变化来决定是否需要重新编译
7. eaccelerator.debug：开启关闭debug日志。如果设置为1，将打印很多文件命中的信息到日志中
8. eaccelerator.filter：用来决定哪个php文件被缓存。可以通过使用通配符（比如”*.php *.phtml”）来匹配需要缓存的php脚本。如果以”!”开头，表示不匹配，这个参数默认是空，比如定义了”!/home”的话，那所有/home目录的脚本都不会被缓存。如果要定义多个匹配，使用空格或者制表符分开，而不是逗号。
9. eaccelerator.shm_max：设置内存缓存可以缓存文件的最大值
10. eaccelerator.shm_ttl：当eAcelerator没有空余的共享内存的时候，就会把最少shm_ttl设置的秒数没访问过的脚本从缓存中释放掉，默认值是0，表示eA不会释放任何缓存。
11. eaccelerator.shm_only：启用或者禁用磁盘缓存。这个选项对session数据和内容的缓存没效果。默认值是0，允许eA使用磁盘和内存进行缓存。
12. eaccelerator.compress：当使用eaccelerator_content_* 的api时，eA可以在缓存前对内容进行压缩。默认值为1表示启用，禁用为0。
13. eaccelerator.compress_level：内容缓存的压缩等级。默认值为9，是最大压缩级别。

 
>注意：如果修改了缓存存放目录需要创建目录并给予deploy.deploy权限

 

## 配置Nginx篇

#### step1：修改nginx.conf文件
	server {
	                listen       801;
	                server_name  www.eycode.com eycode.com;
	                root /data/web/eycode;
	                index index.php index.html index.htm;
	
	        location / {
	                index index.php;
	                proxy_pass http://127.0.0.1:80;
	                proxy_redirect off;
	                proxy_set_header Host $host;
	                proxy_set_header X-Real-IP $remote_addr;
	                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
	                client_max_body_size 10m;
	                client_body_buffer_size 128k;
	                proxy_connect_timeout 90;
	                proxy_read_timeout 90;
	                proxy_buffer_size 4k;
	        }
	
	        location ~ .*\.(gif|jpg|png|bmp|swf|ico|mp3|jpeg|xls|wma)$ {
	                root  /data/web/eycode;
	                expires 30d;
	        }
	
	        location ~ .*\.(js|css|htm)$ {
	                root  /data/web/eycode;
	                expires 1d;
	        }
	}
	[root@ZWN2K-5001 nginx]# ./sbin/nginx
	[root@ZWN2K-5001 nginx]#
	[root@ZWN2K-5001 nginx]# netstat -anput |grep nginx
	tcp 0 0 0.0.0.0:801 0.0.0.0:* LISTEN 17718/nginx

 

>注意：端设置为801是为了测试地址，如果绑定了域名就把端口修改成80即可
