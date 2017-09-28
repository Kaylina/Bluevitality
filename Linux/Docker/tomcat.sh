#!/bin/bash
#版本：tomcat:8.0.43-jre8（需先从官网下载tomcat镜像）
#执行时：WAR包、镜像需在与脚本同一目录下（流程：设置变量、导入镜像、挂载目录、运行容器）
#挂载的目录默认在：/data/docker-tomcat


HOST_TOM_PORT=8089      #Tomcat在宿主机之上暴露的端口
CONTAINER_NAME=tomcat   #容器名
WAR_NAME=signage.war    #WAR包名

#若本地不存在则导入镜像
docker images | grep -q  "docker.io/tomcat" ||  docker load < tomcat.8.0.43-jre8.tar

#若已存在此容器先删除（本脚本未使用dockerfile）
docker rm -f $(docker ps -a | awk "/${CONTAINER_NAME}/{print $1}") 2>&-

#创建资源目录（先清空资源目录数据，防止多次执行起冲突）
rm -rf /data/docker-tomcat/{webapps,config,logs}
mkdir -p /data/docker-tomcat/{webapps,config,logs} 
chcon -Rt svirt_sandbox_file_t /data/docker-tomcat/{webapps,config,logs} 2>&-
setenforce 0 && chmod 766 -R /data/docker-tomcat/{webapps,config,logs}

#移动war包
cp -af ${WAR_NAME} /data/docker-tomcat/webapps

#运行容器
docker run -d -p ${HOST_TOM_PORT}:8080 --name $CONTAINER_NAME \
-v /data/docker-tomcat/webapps:/usr/local/tomcat/webapps -v /data/docker-tomcat/logs:/usr/local/tomcat/logs \
docker.io/tomcat:8.0.43-jre8

# 注：
# 暂时取消了配置文件的挂载：
# -v /data/docker-tomcat-data/config:/usr/local/tomcat/conf \
