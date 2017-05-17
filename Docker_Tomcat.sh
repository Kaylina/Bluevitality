#!/bin/bash
#tomcat: 版本：tomcat:8.0.43-jre8

HOST_TOM_PORT=8089

#若不存在则导入镜像
docker images | grep -q  "docker.io/tomcat" ||  docker load < tomcat.8.0.43-jre8.tar

#若已经存在容器先删除（不存在构建的镜像）
docker rm -f $(docker ps -a | awk '/tomcat/{print $1}') 2> /dev/null

#创建资源目录（先清空资源目录数据，防止多次执行起冲突）
rm -rf /data/docker-tomcat-data/{webapps,config,logs}
mkdir -p /data/docker-tomcat-data/{webapps,config,logs} 
chcon -Rt svirt_sandbox_file_t /data/docker-tomcat-data/{webapps,config,logs} 2>&-
setenforce 0 && chmod 766 -R /data/docker-tomcat-data/{webapps,config,logs}

#移动war包
cp -rf signage.war /data/docker-tomcat-data/webapps

#运行容器
docker run -d -p ${HOST_TOM_PORT}:8080 --name tomcat \
-v /data/docker-tomcat-data/webapps:/usr/local/tomcat/webapps \
-v /data/docker-tomcat-data/logs:/usr/local/tomcat/logs \
docker.io/tomcat:8.0.43-jre8

#------------------------------------------------------------------
#注意：
#暂时取消了挂载：
#-v /data/docker-tomcat-data/config:/usr/local/tomcat/conf \

#结构修改
#限制容器可使用的内存，Tomcat容器的堆大小（百度）
#增加使用注释方法
#
