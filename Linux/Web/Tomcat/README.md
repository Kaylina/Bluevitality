<!-- TOC -->

- [Tomcat实战](#tomcat%E5%AE%9E%E6%88%98)
    - [1. Tomcat简介](#1-tomcat%E7%AE%80%E4%BB%8B)
    - [2. Tomcat安装](#2-tomcat%E5%AE%89%E8%A3%85)
        - [2.1 环境准备](#21-%E7%8E%AF%E5%A2%83%E5%87%86%E5%A4%87)
        - [2.2 部署java环境](#22-%E9%83%A8%E7%BD%B2java%E7%8E%AF%E5%A2%83)
            - [2.2.1 使用tar.gz包部署](#221-%E4%BD%BF%E7%94%A8targz%E5%8C%85%E9%83%A8%E7%BD%B2)
            - [2.2.2 yum安装](#222-yum%E5%AE%89%E8%A3%85)
        - [2.3 安装Tomcat](#23-%E5%AE%89%E8%A3%85tomcat)
        - [2.4 Tomcat目录介绍](#24-tomcat%E7%9B%AE%E5%BD%95%E4%BB%8B%E7%BB%8D)
        - [2.5 启动Tomcat](#25-%E5%90%AF%E5%8A%A8tomcat)
            - [2.5.1 tomcat启动脚本](#251-tomcat%E5%90%AF%E5%8A%A8%E8%84%9A%E6%9C%AC)
        - [2.6 访问网站](#26-%E8%AE%BF%E9%97%AE%E7%BD%91%E7%AB%99)
        - [2.7 Tomcat日志](#27-tomcat%E6%97%A5%E5%BF%97)
    - [3. Tomcat配置文件](#3-tomcat%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6)
        - [3.1 Tomcat配置文件](#31-tomcat%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6)
        - [3.2 Tomcat管理](#32-tomcat%E7%AE%A1%E7%90%86)
        - [3.3 Tomcat主配置文件Server.xml详解](#33-tomcat%E4%B8%BB%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6serverxml%E8%AF%A6%E8%A7%A3)
            - [3.3.1 server.xml组件类别](#331-serverxml%E7%BB%84%E4%BB%B6%E7%B1%BB%E5%88%AB)
            - [3.3.2 组件详解](#332-%E7%BB%84%E4%BB%B6%E8%AF%A6%E8%A7%A3)
            - [3.3.3 配置文件注释](#333-%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6%E6%B3%A8%E9%87%8A)
    - [4. WEB站点部署](#4-web%E7%AB%99%E7%82%B9%E9%83%A8%E7%BD%B2)
        - [4.1 使用war包部署web站点](#41-%E4%BD%BF%E7%94%A8war%E5%8C%85%E9%83%A8%E7%BD%B2web%E7%AB%99%E7%82%B9)
        - [4.2 自定义默认网站目录](#42-%E8%87%AA%E5%AE%9A%E4%B9%89%E9%BB%98%E8%AE%A4%E7%BD%91%E7%AB%99%E7%9B%AE%E5%BD%95)
    - [5. Tomcat多实例及集群架构](#5-tomcat%E5%A4%9A%E5%AE%9E%E4%BE%8B%E5%8F%8A%E9%9B%86%E7%BE%A4%E6%9E%B6%E6%9E%84)
        - [5.1 Tomcat多实例](#51-tomcat%E5%A4%9A%E5%AE%9E%E4%BE%8B)
            - [5.1.1 复制Tomcat目录](#511-%E5%A4%8D%E5%88%B6tomcat%E7%9B%AE%E5%BD%95)
            - [5.1.2 修改配置文件](#512-%E4%BF%AE%E6%94%B9%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6)
            - [5.1.3 启动多实例](#513-%E5%90%AF%E5%8A%A8%E5%A4%9A%E5%AE%9E%E4%BE%8B)
        - [5.2 Tomcat集群](#52-tomcat%E9%9B%86%E7%BE%A4)
    - [6. Tomcat监控](#6-tomcat%E7%9B%91%E6%8E%A7)
        - [tomcat远程监控](#tomcat%E8%BF%9C%E7%A8%8B%E7%9B%91%E6%8E%A7)
        - [使用zabbix监控tomcat](#%E4%BD%BF%E7%94%A8zabbix%E7%9B%91%E6%8E%A7tomcat)
    - [7. Tomcat安全优化和性能优化](#7-tomcat%E5%AE%89%E5%85%A8%E4%BC%98%E5%8C%96%E5%92%8C%E6%80%A7%E8%83%BD%E4%BC%98%E5%8C%96)
        - [7.1 安全优化](#71-%E5%AE%89%E5%85%A8%E4%BC%98%E5%8C%96)
        - [7.2 性能优化](#72-%E6%80%A7%E8%83%BD%E4%BC%98%E5%8C%96)
            - [7.2.1 屏蔽dns查询enableLookups="false"](#721-%E5%B1%8F%E8%94%BDdns%E6%9F%A5%E8%AF%A2enablelookupsfalse)
            - [7.2.2 jvm调优](#722-jvm%E8%B0%83%E4%BC%98)

<!-- /TOC -->

# Tomcat实战

## 1. Tomcat简介

```txt
Tomcat是Apache软件基金会（Apache Software Foundation）的Jakarta 项目中的一个核心项目，由Apache、Sun和其他一些公司及个人共同开发而成。

Tomcat服务器是一个免费的开放源代码的Web应用服务器，属于轻量级应用服务器，在中小型系统和并发访问用户不是很多的场合下被普遍使用，是开发和调试JSP程序的首选。

Tomcat和Nginx、Apache(httpd)、lighttpd等Web服务器一样，具有处理HTML页面的功能，另外它还是一个Servlet和JSP容器，独立的Servlet容器是Tomcat的默认模式。不过，Tomcat处理静态HTML的能力不如Nginx/Apache服务器。
```

> 对比php软件，区别？
> 目前Tomcat最新版本为9.0。Java容器还有resin、weblogic等。

## 2. Tomcat安装

### 2.1 环境准备

```bash
    JDK下载：http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html
    Tomcat下载：http://tomcat.apache.org/
    因为jdk和Tomcat的版本对运维来说没什么区别，提供本文使用的软件下载地址：http://pan.baidu.com/s/1IpioA

    # 系统版本
    [root@centos7 ~]# cat /etc/redhat-release
    CentOS Linux release 7.2.1511 (Core)
    [root@centos7 ~]# uname -r
    3.10.0-327.36.3.el7.x86_64
    # IP地址
    [root@centos7 ~]# ip a s eth0
    2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
        link/ether 00:0c:29:3a:65:a8 brd ff:ff:ff:ff:ff:ff
        inet 10.0.0.77/24 brd 10.0.0.255 scope global eth0
        valid_lft forever preferred_lft forever
        inet6 fe80::20c:29ff:fe3a:65a8/64 scope link
        valid_lft forever preferred_lft forever
```

### 2.2 部署java环境

#### 2.2.1 使用tar.gz包部署

```bash
    [root@centos7 ~]# mkdir src
    [root@centos7 ~]# cd src/
    [root@centos7 src]# rz

    [root@centos7 src]# mkdir /application/
    [root@centos7 src]# tar xf jdk-8u60-linux-x64.tar.gz -C /application/
    [root@centos7 src]# ln -s /application/jdk1.8.0_60/ /application/jdk
    [root@centos7 src]# sed -i.ori '$a export JAVA_HOME=/application/jdk\nexport PATH=$JAVA_HOME/bin:$JAVA_HOME/jre/bin:$PATH\nexport CLASSPATH=.$CLASSPATH:$JAVA_HOME/lib:$JAVA_HOME/jre/lib:$JAVA_HOME/lib/tools.jar' /etc/profile

    [root@centos7 src]# source /etc/profile
    ## 如果能查到java版本，证明java部署成功
    [root@centos7 src]# java -version
    java version "1.8.0_60"
    Java(TM) SE Runtime Environment (build 1.8.0_60-b27)
    Java HotSpot(TM) 64-Bit Server VM (build 25.60-b23, mixed mode)
```

#### 2.2.2 yum安装

```bash
    # install
    yum install java -y
    # check
    java -version
```

### 2.3 安装Tomcat

```bash
    [root@centos7 src]# tar xf apache-tomcat-8.0.27.tar.gz -C /application/
    [root@centos7 src]# ln -s /application/apache-tomcat-8.0.27 /application/tomcat
    [root@centos7 src]# echo 'export TOMCAT_HOME=/application/tomcat'>>/etc/profile
    [root@centos7 src]# source /etc/profile
    [root@centos7 src]# chown -R root.root /application/jdk/ /application/tomcat/

    ## 一键搞定
    tar xf apache-tomcat-8.0.27.tar.gz -C /application/
    ln -s /application/apache-tomcat-8.0.27 /application/tomcat
    echo 'export TOMCAT_HOME=/application/tomcat'>>/etc/profile
    source /etc/profile
    chown -R root.root /application/jdk/ /application/tomcat/

    [root@centos7 src]# tail -4 /etc/profile
    export JAVA_HOME=/application/jdk
    export PATH=$JAVA_HOME/bin:$JAVA_HOME/jre/bin:$PATH
    export CLASSPATH=.$CLASSPATH:$JAVA_HOME/lib:$JAVA_HOME/jre/lib:$JAVA_HOME/lib/tools.jar
    export TOMCAT_HOME=/application/tomcat
```

### 2.4 Tomcat目录介绍

```bash
    [root@centos7 src]# cd /application/tomcat/
    [root@centos7 tomcat]# tree -L 1
    .
    ├── bin            # 用以启动、关闭Tomcat或者其它功能的脚本（.bat文件和.sh文件）
    ├── conf           # 用以配置Tomcat的XML及DTD文件
    ├── lib            # 存放web应用能访问的JAR包
    ├── LICENSE
    ├── logs           # Catalina和其它Web应用程序的日志文件
    ├── NOTICE
    ├── RELEASE-NOTES
    ├── RUNNING.txt
    ├── temp           # 临时文件
    ├── webapps        # Web应用程序根目录
    └── work           # 用以产生有JSP编译出的Servlet的.java和.class文件

    7 directories, 4 files

    [root@centos7 tomcat]# cd webapps/
    [root@centos7 webapps]# ll
    total 8
    drwxr-xr-x 14 root root 4096 Dec 11 01:40 docs         # tomcat帮助文档
    drwxr-xr-x  6 root root   78 Dec 11 01:40 examples     # web应用实例
    drwxr-xr-x  5 root root   82 Dec 11 01:40 host-manager # 管理
    drwxr-xr-x  5 root root   97 Dec 11 01:40 manager      # 管理
    drwxr-xr-x  3 root root 4096 Dec 11 01:40 ROOT         # 默认网站根目录
```

### 2.5 启动Tomcat

```bash
    # 启动程序/application/tomcat/bin/startup.sh
    # 关闭程序/application/tomcat/bin/shutdown.sh

    [root@centos7 ~]# /application/tomcat/bin/startup.sh
    Using CATALINA_BASE:   /application/tomcat
    Using CATALINA_HOME:   /application/tomcat
    Using CATALINA_TMPDIR: /application/tomcat/temp
    Using JRE_HOME:        /application/jdk
    Using CLASSPATH:       /application/tomcat/bin/bootstrap.jar:/application/tomcat/bin/tomcat-juli.jar
    Tomcat started.

    [root@centos7 ~]# netstat -tunlp|grep java
    tcp6       0      0 :::8080                 :::*                    LISTEN      9857/java
    tcp6       0      0 :::8009                 :::*                    LISTEN      9857/java

    [root@centos7 ~]# ps -ef|grep [j]ava
    root       9857      1 21 01:47 pts/1    00:00:13 /application/jdk/binjava -Djava.util.logging.config.file=/application/tomcat/conf/logging.properties -Djava.util.logging.manager=org.apache.juli.ClassLoaderLogManager -Djava.endorsed.dirs=/application/tomcat/endorsed -classpath /application/tomcat/bin/bootstrap.jar:/application/tomcat/bin/tomcat-juli.jar -Dcatalina.base=/application/tomcat -Dcatalina.home=/application/tomcat -Djava.io.tmpdir=/application/tomcat/temp org.apache.catalina.startup.Bootstrap start
```

#### 2.5.1 tomcat启动脚本

```bash
    # 适用于Sysvinit技术，多实例需要完善
    [root@centos7 ~]# cat tomcat
    #!/bin/sh
    #
    # tomcat          Start/Stop the tomcat daemon.
    #
    # chkconfig: 2345 85 60
    # description:  The Apache Tomcat® software is an open source implementation of the Java Servlet, JavaServer Pages, Java Expression Language and Java WebSocket technologies. The Java Servlet, JavaServer Pages, Java Expression Language and Java WebSocket specifications are developed under the Java Community Process. 

    prog="tomcat"
    tomcat="/application/tomcat/bin/"
    tomcat1="/application/tomcat8_1/bin/"
    tomcat2="/application/tomcat8_2/bin/"
    lockfile=/var/lock/subsys/tomcat

    # Source function library.
    . /etc/rc.d/init.d/functions

    start() {
        if [ $UID -ne 0 ] ; then
            echo "User has insufficient privilege."
            exit 4
        fi
        $tomcat/startup.sh &&\
        success && echo  
    }

    stop() {
        if [ $UID -ne 0 ] ; then
            echo "User has insufficient privilege."
            exit 4
        fi
        $tomcat/shutdown.sh &&\
        success && echo $"Stopping $prog" 
    }

    restart() {
        stop &&\
        start
    }

    configtest(){
        $tomcat/configtest.sh
    }

    case "$1" in
        start)
            $1
            ;;
        stop)
            $1
            ;;
        restart)
            $1
            ;;
        configtest)
            $1
            ;;
        *)
            echo $"Usage: $0 {start|stop|status|restart|configtest}"
            exit 2
    esac
```

### 2.6 访问网站

    网址：http://10.0.0.77:8080/
    ![tomcat1](http://i.imgur.com/ZfUDq3t.png)

### 2.7 Tomcat日志

```bash
    [root@centos7 ~]# cd /application/tomcat/logs/
    [root@centos7 logs]# ls
    catalina.2016-12-11.log      localhost.2016-12-11.log
    catalina.out                 localhost_access_log.2016-12-11.txt
    host-manager.2016-12-11.log  manager.2016-12-11.log

    # tomcat实时日志
    [root@centos7 logs]# tailf catalina.out
    11-Dec-2016 01:48:50.698 INFO [localhost-startStop-1] org.apache.catalina.startup.HostConfig.deployDirectory Deployment of web application directory /application/apache-tomcat-8.0.27/webapps/docs has finished in 186 ms
    11-Dec-2016 01:48:50.698 INFO [localhost-startStop-1] org.apache.catalina.startup.HostConfig.deployDirectory Deploying web application directory /application/apache-tomcat-8.0.27/webapps/examples
    11-Dec-2016 01:48:57.313 INFO [localhost-startStop-1] org.apache.catalina.startup.HostConfig.deployDirectory Deployment of web application directory /application/apache-tomcat-8.0.27/webapps/examples has finished in 6,615 ms
    11-Dec-2016 01:48:57.314 INFO [localhost-startStop-1] org.apache.catalina.startup.HostConfig.deployDirectory Deploying web application directory /application/apache-tomcat-8.0.27/webapps/host-manager
    11-Dec-2016 01:48:58.131 INFO [localhost-startStop-1] org.apache.catalina.startup.HostConfig.deployDirectory Deployment of web application directory /application/apache-tomcat-8.0.27/webapps/host-manager has finished in 814 ms
    11-Dec-2016 01:48:58.184 INFO [localhost-startStop-1] org.apache.catalina.startup.HostConfig.deployDirectory Deploying web application directory /application/apache-tomcat-8.0.27/webapps/manager
    11-Dec-2016 01:48:58.555 INFO [localhost-startStop-1] org.apache.catalina.startup.HostConfig.deployDirectory Deployment of web application directory /application/apache-tomcat-8.0.27/webapps/manager has finished in 422 ms
    11-Dec-2016 01:48:58.614 INFO [main] org.apache.coyote.AbstractProtocol.start Starting ProtocolHandler ["http-nio-8080"]
    11-Dec-2016 01:48:58.683 INFO [main] org.apache.coyote.AbstractProtocol.start Starting ProtocolHandler ["ajp-nio-8009"]
    11-Dec-2016 01:48:58.762 INFO [main] org.apache.catalina.startup.Catalina.start Server startup in 59801 ms
```

## 3. Tomcat配置文件

### 3.1 Tomcat配置文件

```bash
    [root@centos7 conf]# pwd
    /application/tomcat/conf
    [root@centos7 conf]# ll -h
    total 212K
    drwxr-xr-x 3 root root   22 Dec 11 01:47 Catalina
    -rw------- 1 root root  13K Sep 28  2015 catalina.policy
    -rw------- 1 root root 7.0K Sep 28  2015 catalina.properties
    -rw------- 1 root root 1.6K Sep 28  2015 context.xml
    -rw------- 1 root root 3.4K Sep 28  2015 logging.properties
    -rw------- 1 root root 6.4K Sep 28  2015 server.xml
    -rw------- 1 root root 1.8K Sep 28  2015 tomcat-users.xml
    -rw------- 1 root root 1.9K Sep 28  2015 tomcat-users.xsd
    -rw------- 1 root root 164K Sep 28  2015 web.xml
```

### 3.2 Tomcat管理

> 测试功能，生产环境不要用。

```bash
    Tomcat管理功能用于对Tomcat自身以及部署在Tomcat上的应用进行管理的web应用。在默认情况下是处于禁用状态的。如果需要开启这个功能，就需要配置管理用户，即配置前面说过的tomcat-users.xml。

    [root@centos7 conf]# vim /application/tomcat/conf/tomcat-users.xml

    [root@centos7 conf]# tail -4 /application/tomcat/conf/tomcat-users.xml
        <role rolename="manager-gui"/>
        <role rolename="admin-gui"/>
        <user username="tomcat" password="tomcat" roles="manager-gui,admin-gui"/>
    </tomcat-users>  # 在此行前加入上面三行

    [root@centos7 conf]# /application/tomcat/bin/shutdown.sh
    Using CATALINA_BASE:   /application/tomcat
    Using CATALINA_HOME:   /application/tomcat
    Using CATALINA_TMPDIR: /application/tomcat/temp
    Using JRE_HOME:        /application/jdk
    Using CLASSPATH:       /application/tomcat/bin/bootstrap.jar:/application/tomcat/bin/tomcat-juli.jar

    [root@centos7 conf]# /application/tomcat/bin/startup.sh
    Using CATALINA_BASE:   /application/tomcat
    Using CATALINA_HOME:   /application/tomcat
    Using CATALINA_TMPDIR: /application/tomcat/temp
    Using JRE_HOME:        /application/jdk
    Using CLASSPATH:       /application/tomcat/bin/bootstrap.jar:/application/tomcat/bin/tomcat-juli.jar
    Tomcat started.
```
![Tomcat2](http://i.imgur.com/gJcujWB.png)

### 3.3 Tomcat主配置文件Server.xml详解

#### 3.3.1 server.xml组件类别

```txt
    顶级组件：位于整个配置的顶层，如server。
    容器类组件：可以包含其它组件的组件，如service、engine、host、context。
    连接器组件：连接用户请求至tomcat，如connector。
    被嵌套类组件：位于一个容器当中，不能包含其他组件，如Valve、logger。

    <server>
         <service>
         <connector />
         <engine>
         <host>
         <context></context>
         </host>
         <host>
         <context></context>
         </host>
         </engine>
         </service>
    </server>
```

#### 3.3.2 组件详解

* engine：核心容器组件，catalina引擎，负责通过connector接收用户请求，并处理请求，将请求转至对应的虚拟主机host。
* host：类似于httpd中的虚拟主机，一般而言支持基于FQDN的虚拟主机。
* context：定义一个应用程序，是一个最内层的容器类组件（不能再嵌套）。配置context的主要目的指定对应对的webapp的根目录，类似于httpd的alias，其还能为webapp指定额外的属性，如部署方式等。
* connector：接收用户请求，类似于httpd的listen配置监听端口的。
* service（服务）：将connector关联至engine，因此一个service内部可以有多个connector，但只能有一个引擎engine。service内部有两个connector，一个engine。因此，一般情况下一个server内部只有一个service，一个service内部只有一个engine，但一个service内部可以有多个connector。
* server：表示一个运行于JVM中的tomcat实例。
* Valve：阀门，拦截请求并在将其转至对应的webapp前进行某种处理操作，可以用于任何容器中，比如记录日志(access log valve)、基于IP做访问控制(remote address filter valve)。
* logger：日志记录器，用于记录组件内部的状态信息，可以用于除context外的任何容器中。
* realm：可以用于任意容器类的组件中，关联一个用户认证库，实现认证和授权。可以关联的认证库有两种：UserDatabaseRealm、MemoryRealm和JDBCRealm。
* UserDatabaseRealm：使用JNDI自定义的用户认证库。
* MemoryRealm：认证信息定义在tomcat-users.xml中。
* JDBCRealm：认证信息定义在数据库中，并通过JDBC连接至数据库中查找认证用户。

#### 3.3.3 配置文件注释

```xml
    <?xml version='1.0' encoding='utf-8'?>
    <!--
    <Server>元素代表整个容器,是Tomcat实例的顶层元素.由org.apache.catalina.Server接口来定义.它包含一个<Service>元素.并且它不能做为任何元素的子元素.
        port指定Tomcat监听shutdown命令端口.终止服务器运行时,必须在Tomcat服务器所在的机器上发出shutdown命令.该属性是必须的.
        shutdown指定终止Tomcat服务器运行时,发给Tomcat服务器的shutdown监听端口的字符串.该属性必须设置，
        *****优化方式，可以将端口修改为其他端口，关闭字符修改为其他字符。
    -->
    <Server port="8005" shutdown="SHUTDOWN">
      <Listener className="org.apache.catalina.startup.VersionLoggerListener" />
      <Listener className="org.apache.catalina.core.AprLifecycleListener" SSLEngine="on" />
      <Listener className="org.apache.catalina.core.JreMemoryLeakPreventionListener" />
      <Listener className="org.apache.catalina.mbeans.GlobalResourcesLifecycleListener" />
      <Listener className="org.apache.catalina.core.ThreadLocalLeakPreventionListener" />
      <GlobalNamingResources>
        <Resource name="UserDatabase" auth="Container"
                  type="org.apache.catalina.UserDatabase"
                  description="User database that can be updated and saved"
                  factory="org.apache.catalina.users.MemoryUserDatabaseFactory"
                  pathname="conf/tomcat-users.xml" />
      </GlobalNamingResources>
      <!--service服务组件-->
      <Service name="Catalina">
        <!--
        connector：接收用户请求，类似于httpd的listen配置监听端口.
            port指定服务器端要创建的端口号，并在这个端口监听来自客户端的请求。
            address：指定连接器监听的地址，默认为所有地址（即0.0.0.0）
            protocol连接器使用的协议，支持HTTP和AJP。AJP（Apache Jserv Protocol）专用于tomcat与apache建立通信的， 在httpd反向代理用户请求至tomcat时使用（可见Nginx反向代理时不可用AJP协议）。
            minProcessors服务器启动时创建的处理请求的线程数
            maxProcessors最大可以创建的处理请求的线程数
            enableLookups如果为true，则可以通过调用request.getRemoteHost()进行DNS查询来得到远程客户端的实际主机名，若为false则不进行DNS查询，而是返回其ip地址
            redirectPort指定服务器正在处理http请求时收到了一个SSL传输请求后重定向的端口号
            acceptCount指定当所有可以使用的处理请求的线程数都被使用时，可以放到处理队列中的请求数，超过这个数的请求将不予处理
            connectionTimeout指定超时的时间数(以毫秒为单位)
        -->
        <Connector port="8080" protocol="HTTP/1.1"
                   connectionTimeout="20000"
                   redirectPort="8443" />
        <Connector port="8009" protocol="AJP/1.3" redirectPort="8443" />
        <!--AJP是一种协议，如果使用nginx和tomcat，他们之间通信是通过http协议，就可以注释上条-->
        <!--engine,核心容器组件,catalina引擎,负责通过connector接收用户请求,并处理请求,将请求转至对应的虚拟主机host
            defaultHost指定缺省的处理请求的主机名，它至少与其中的一个host元素的name属性值是一样的
        -->
        <Engine name="Catalina" defaultHost="localhost">
          <!--Realm表示存放用户名，密码及role的数据库-->
          <Realm className="org.apache.catalina.realm.LockOutRealm">
            <Realm className="org.apache.catalina.realm.UserDatabaseRealm"
                   resourceName="UserDatabase"/>
          </Realm>
          <!--
          host表示一个虚拟主机
            name指定主机名
            appBase应用程序基本目录，即存放应用程序的目录.一般为appBase="webapps" ，相对于CATALINA_HOME而言的，也可以写绝对路径。
            unpackWARs如果为true，则tomcat会自动将WAR文件解压，否则不解压，直接从WAR文件中运行应用程序
            autoDeploy：在tomcat启动时，是否自动部署。
            xmlValidation：是否启动xml的校验功能，一般xmlValidation="false"。
            xmlNamespaceAware：检测名称空间，一般xmlNamespaceAware="false"。
          -->
          <Host name="localhost"  appBase="webapps"
                unpackWARs="true" autoDeploy="true">
            <!--
            Context表示一个web应用程序，通常为WAR文件
                docBase应用程序的路径或者是WAR文件存放的路径,也可以使用相对路径，起始路径为此Context所属Host中appBase定义的路径。
                path表示此web应用程序的url的前缀，这样请求的url为http://localhost:8080/path/****
                reloadable这个属性非常重要，如果为true，则tomcat会自动检测应用程序的/WEB-INF/lib 和/WEB-INF/classes目录的变化，自动装载新的应用程序，可以在不重启tomcat的情况下改变应用程序
            -->
            <Context path="" docBase="" debug=""/>
            <Valve className="org.apache.catalina.valves.AccessLogValve" directory="logs"
                   prefix="localhost_access_log" suffix=".txt"
                   pattern="%h %l %u %t &quot;%r&quot; %s %b" />
          </Host>
        </Engine>
      </Service>
    </Server>
```

## 4. WEB站点部署

> 上线的代码有两种方式，第一种方式是直接将程序目录放在webapps目录下面，这种方式大家已经明白了，就不多说了。第二种方式是使用开发工具将程序打包成war包，然后上传到webapps目录下面。下面让我们见识一下这种方式。

### 4.1 使用war包部署web站点

```bash
    [root@centos7 webapps]# pwd
    /application/tomcat/webapps
    [root@centos7 webapps]# rz   # 上传memtest.war，此文件也在上面的百度网盘里
    [root@centos7 webapps]#
    [root@centos7 webapps]# ls
    docs  examples  host-manager  manager  memtest  memtest.war  ROOT
    自动生成一个memtest目录

    浏览器访问：`http://10.0.0.77:8080/memtest/meminfo.jsp`
```
![Tomcat3](http://i.imgur.com/XPCWXvY.png)

### 4.2 自定义默认网站目录

> 上面访问的网址为http://10.0.0.77:8080/memtest/meminfo.jsp

> 现在我想访问格式为http://10.0.0.77:8080/meminfo.jsp

> 怎么做？

> 方法一

    将meminfo.jsp或其他程序放在tomcat/webapps/ROOT目录下即可。因为默认网站根目录为tomcat/webapps/ROOT

> 方法二

```bash
    [root@centos7 ~]# vim /application/tomcat/conf/server.xml
          <Host name="localhost"  appBase="webapps"
                unpackWARs="true" autoDeploy="true">
             <Context path="" docBase="/application/tomcat/webapps/memtest" debug="0" reloadable="false" crossContext="true"/>
    [root@centos7 ~]# /application/tomcat/bin/shutdown.sh
    [root@centos7 ~]# /application/tomcat/bin/startup.sh
```

## 5. Tomcat多实例及集群架构

### 5.1 Tomcat多实例

#### 5.1.1 复制Tomcat目录

```bash
    [root@centos7 ~]# cd /application/
    [root@centos7 application]# cp -a apache-tomcat-8.0.27 tomcat8_1
    [root@centos7 application]# cp -a apache-tomcat-8.0.27 tomcat8_2
```

#### 5.1.2 修改配置文件

```bash
    [root@centos7 application]# mkdir -p /data/www/www/ROOT
    [root@centos7 application]# cp /application/tomcat/webapps/memtest/meminfo.jsp /data/www/www/ROOT/
    [root@centos7 application]# sed -i '22s#8005#8011#;69s#8080#8081#;123s#appBase=".*"# appBase="/data/www/www"#' /application/tomcat8_1/conf/server.xml
    [root@centos7 application]# sed -i '22s#8005#8012#;69s#8080#8082#;123s#appBase=".*"# appBase="/data/www/www"#' /application/tomcat8_2/conf/server.xml

    [root@centos7 application]# diff /application/tomcat/conf/server.xml  /application/tomcat8_1/conf/server.xml
    22c22
    < <Server port="8005" shutdown="SHUTDOWN">
    ---
    > <Server port="8011" shutdown="SHUTDOWN">
    69c69
    <     <Connector port="8080" protocol="HTTP/1.1"
    ---
    >     <Connector port="8081" protocol="HTTP/1.1"
    123c123
    <       <Host name="localhost"  appBase="webapps"
    ---
    >       <Host name="localhost"   appBase="/data/www/www"

    [root@centos7 application]# diff /application/tomcat/conf/server.xml  /application/tomcat8_2/conf/server.xml
    22c22
    < <Server port="8005" shutdown="SHUTDOWN">
    ---
    > <Server port="8012" shutdown="SHUTDOWN">
    69c69
    <     <Connector port="8080" protocol="HTTP/1.1"
    ---
    >     <Connector port="8082" protocol="HTTP/1.1"
    123c123
    <       <Host name="localhost"  appBase="webapps"
    ---
    >       <Host name="localhost"   appBase="/data/www/www"
```

#### 5.1.3 启动多实例

```bash
    [root@centos7 application]# for i in {1..2};do /application/tomcat8_$i/bin/startup.sh;done
    [root@centos7 application]# netstat -tunlp|grep java
    tcp6       0      0 :::8080                 :::*                    LISTEN      9940/java
    tcp6       0      0 :::8081                 :::*                    LISTEN      10035/java
    tcp6       0      0 :::8082                 :::*                    LISTEN      10045/java
    tcp6       0      0 127.0.0.1:8005          :::*                    LISTEN      9940/java
    tcp6       0      0 :::8009                 :::*                    LISTEN      9940/java
```

> 浏览器可以分别访问http://10.0.0.77:8081/meminfo.jsp 和 http://10.0.0.77:8082/meminfo.jsp

### 5.2 Tomcat集群

> 使用nginx+Tomcat反向代理集群，通过nginx反向代理实现

```bash
    本地安装nginx，配置如下：
    [root@centos7 ~]# vim /application/nginx/conf/nginx.conf
    worker_processes  1;
    events {
        worker_connections  1024;
    }
    http {
        include       mime.types;
        default_type  application/octet-stream;
        sendfile        on;
        keepalive_timeout  65;

        upstream web_pools {
            server 127.0.0.1:8080;
            server 127.0.0.1:8081;
            server 127.0.0.1:8082;
        }

        server {
            listen       80;
            server_name  localhost;
            location / {
                root   html;
                index  index.jsp index.html index.htm;
                proxy_pass http://web_pools;
            }
        }
    }
    [root@centos7 ~]# /application/nginx/sbin/nginx -t
    [root@centos7 ~]# /application/nginx/sbin/nginx
```

> 浏览器可以访问http://10.0.0.77/meminfo.jsp, 已实现tomcat集群

## 6. Tomcat监控

1. Tomcat自带函数检测
2. jps命令
3. jstack
4. jmap
5. jconsole和jvisualvm
6. zabbix

> 企业案例：Linux下java/http进程高解决案例

> 生产环境下某台tomcat7服务器，在刚发布时的时候一切都很正常，在运行一段时间后就出现CPU占用很高的问题，基本上是负载一天比一天高。请搞定！

```txt
    问题分析：
    1 程序属于CPU密集型，和开发沟通过，排除此类情况。
    2 程序代码有问题，出现死循环，可能性极大。

    问题解决：
    1 开发那边无法排查代码某个模块有问题，从日志上也无法分析得出。
    2 记得原来通过strace跟踪的方法解决了一台PHP服务器CPU占用高的问题，但是通过这种方法无效，经过google搜索，发现可以通过下面的方法进行解决。

    解决过程：
    1 根据top命令，发现PID为2633的Java进程占用CPU高达300%，出现故障。
    2 找到该进程后，如何定位具体线程或代码呢，首先显示线程列表,并按照CPU占用高的线程排序：
    [root@localhost logs]# ps -mp 2633 -o THREAD,tid,time|sort -rn
    显示结果如下：
    USER     %CPU PRI SCNT WCHAN  USER SYSTEM   TID     TIME
    root     10.5  19    - -         -      -  3626 00:12:48
    root     10.1  19    - -         -      -  3593 00:12:16
    找到了耗时最高的线程3626，占用CPU时间有12分钟了！
    将需要的线程ID转换为16进制格式：
    [root@localhost logs]# printf "%x\n" 3626
    e18
    最后打印线程的堆栈信息：
    [root@localhost logs]# jstack 2633 | grep e18 -A 30
    将输出的信息发给开发部进行确认，这样就能找出有问题的代码。
```

### tomcat远程监控

```bash
    [root@backup ~]# vim /application/tomcat/bin/catalina.sh

    97 CATALINA_OPTS="$CATALINA_OPTS
    98 -Dcom.sun.management.jmxremote
    99 -Dcom.sun.management.jmxremote.port=12345
    100 -Dcom.sun.management.jmxremote.authenticate=false
    101 -Dcom.sun.management.jmxremote.ssl=false
    102 -Djava.rmi.server.hostname=10.0.0.41"   ## ip地址

    ## 需要做host解析

```

![jconsole1](http://imgur.com/a/gc1Z5)

### 使用zabbix监控tomcat

> zabbix监控tomcat通过JMX interfaces监控

条件：
1. zabbix-server开启JavaGateway
2. tomcat开启远程监控，注意端口
3. web配置jmx接口，添加模板

```bash
zabbix-server配置，配置后重启zabbix-server
sed -i -e '217a JavaGateway=127.0.0.1' -e '225a JavaGatewayPort=10052'  -e '235a StartJavaPollers=5' /etc/zabbix/zabbix_server.conf

## 启动zabbix-java-gateway
[root@m01 ~]# /etc/init.d/zabbix-java-gateway start

```



## 7. Tomcat安全优化和性能优化

### 7.1 安全优化

* 降权启动
* telnet管理端口保护
* ajp连接端口保护
* 禁用管理端

### 7.2 性能优化

#### 7.2.1 屏蔽dns查询enableLookups="false"

```xml
        <Connector  port="8081" protocol="HTTP/1.1"
                   connectionTimeout="6000" enableLookups="false" acceptCount="800"
                   redirectPort="8443" />
```

#### 7.2.2 jvm调优

> Tomcat最吃内存，只要内存足够，这只猫就跑的很快。
> 如果系统资源有限，那就需要进行调优，提高资源使用率。

```txt
    优化catalina.sh配置文件。在catalina.sh配置文件中添加以下代码：
    ## 根据内存大小修改，1G内存的标配：注意加载配置文件前几行，因为是配置变量，放脚本后面就没有效果了
    JAVA_OPTS="-Djava.awt.headless=true -Dfile.encoding=UTF-8 -server -Xms1024m -Xmx1024m -XX:NewSize=512m -XX:MaxNewSize=512m -XX:PermSize=512m -XX:MaxPermSize=512m"
    server:一定要作为第一个参数，在多个CPU时性能佳
    -Xms：初始堆内存Heap大小，使用的最小内存,cpu性能高时此值应设的大一些
    -Xmx：初始堆内存heap最大值，使用的最大内存
    上面两个值是分配JVM的最小和最大内存，取决于硬件物理内存的大小，建议均设为物理内存的一半。
    -XX:PermSize:设定内存的永久保存区域
    -XX:MaxPermSize:设定最大内存的永久保存区域
    -XX:MaxNewSize:
    -Xss 15120 这使得JBoss每增加一个线程（thread)就会立即消耗15M内存，而最佳值应该是128K,默认值好像是512k.
    +XX:AggressiveHeap 会使得 Xms没有意义。这个参数让jvm忽略Xmx参数,疯狂地吃完一个G物理内存,再吃尽一个G的swap。
    -Xss：每个线程的Stack大小
    -verbose:gc 现实垃圾收集信息
    -Xloggc:gc.log 指定垃圾收集日志文件
    -Xmn：young generation的heap大小，一般设置为Xmx的3、4分之一
    -XX:+UseParNewGC ：缩短minor收集的时间
    -XX:+UseConcMarkSweepGC ：缩短major收集的时间
```