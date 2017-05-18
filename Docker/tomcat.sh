#!/bin/bash
#tomcat: �汾��tomcat:8.0.43-jre8����Ҫ�ȴӹ�������tomcat����
#�ű�ִ��ʱ��WAR����������Ҫ�ڽű�ͬһĿ¼��(���̣����ñ��������뾵�񡢹���Ŀ¼����������)
#���ص�Ŀ¼Ĭ���ڣ�/data/docker-tomcat


HOST_TOM_PORT=8089      #Tomcat�������������Ķ˿�
CONTAINER_NAME=tomcat   #������
WAR_NAME=signage.war    #WAR����

#�����������뾵��
docker images | grep -q  "docker.io/tomcat" ||  docker load < tomcat.8.0.43-jre8.tar

#���Ѵ��ڴ�������ɾ�������ű�û��ʹ��dockerfile��ʽ��
docker rm -f $(docker ps -a | awk "/${CONTAINER_NAME}/{print $1}") 2>&-

#������ԴĿ¼���������ԴĿ¼���ݣ���ֹ���ִ�����ͻ��
rm -rf /data/docker-tomcat/{webapps,config,logs}
mkdir -p /data/docker-tomcat/{webapps,config,logs} 
chcon -Rt svirt_sandbox_file_t /data/docker-tomcat/{webapps,config,logs} 2>&-
setenforce 0 && chmod 766 -R /data/docker-tomcat/{webapps,config,logs}

#�ƶ�war��
cp -rf ${WAR_NAME} /data/docker-tomcat/webapps

#��������
docker run -d -p ${HOST_TOM_PORT}:8080 --name $CONTAINER_NAME \
-v /data/docker-tomcat/webapps:/usr/local/tomcat/webapps -v /data/docker-tomcat/logs:/usr/local/tomcat/logs \
docker.io/tomcat:8.0.43-jre8

#------------------------------------------------------------------
# ע�⣺
# ��ʱȡ���˹��أ�
# -v /data/docker-tomcat-data/config:/usr/local/tomcat/conf \
 
# �ṹ�޸�
# ����������ʹ�õ��ڴ棬Tomcat�����ĶѴ�С���ٶȣ�
#