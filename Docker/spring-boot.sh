#!/bin/bash
#jar���������ļ���Ҫ�ڵ�ǰĿ¼��

#DMS������Ҫ�Ķ˿ڣ��������Ѿ�ʹ�õĶ˿ڳ�ͻ�����޸���war����EMQ�ĵ�ַҲҪ�޸ģ�
SERV_PORT=8011
#���ݿ�����IP��ַ���˺�����
DB_ADDRESS=139.196.238.XX
#emq��������ַ
EMQ_ADDRESS=139.196.238.xx
#���鱣��Ĭ�ϣ�����������޸�ID..��
EMQ_ID=$(echo ${RANDOM} | cut -c 1-2)

#---------------------------------------------------------------------------------------------------
#����Ĭ�Ͼ��������ڲ����أ�
docker images | grep -q openjdk || docker load < openjre.8.tar
#ɾ���Ѿ������������͹����ľ���
docker rm -f $(docker ps -a | awk '/paybay-dms-spring-boot/{print $1}' ) 2> /dev/null 
docker rmi $(docker images | awk '/paybay-dms/{print $3}') 2> dev/null

sed -Ei  "1,9s#[0-9]{2,}\.[0-9]+\.[0-9]+\.[0-9]+#${DB_ADDRESS:?var not define}#g" application.properties
sed -Ei  "1,9s#[0-9]{2,}\.[0-9]+\.[0-9]+\.[0-9]+#${EMQ_ADDRESS:?var not define}#g" common.properties
sed -Ei  "s#id=(..........).*#id=\1${EMQ_ID}#" common.properties
echo -e '\033[32mconfiguration modified successfully!... \033[0m' || { echo -e  '\033[31mconfiguration modified fail!... \033[0m' ; exit 1 ; }
#����dockerfile�����������ļ�&��������ʱִ�е����
cat > dockerfile <<eof
FROM docker.io/openjdk:8-jre
ADD paybay-dms-1.0.0.jar  /tmp/paybay-dms-1.0.0.jar
ADD common.properties   /tmp/common.properties
ADD application.properties  /tmp/application.properties
VOLUME /dms/logs/dms /logs/dms
EXPOSE ${SERV_PORT:=8011}
WORKDIR /tmp
CMD java -jar -Dproperty.config.location=/tmp/ /tmp/paybay-dms-1.0.0.jar --spring.config.location=/tmp/
eof
#��������
docker build -t  paybay-dms-spring-boot  .
#����������
docker run -p ${SERV_PORT}:${SERV_PORT} -d  paybay-dms-spring-boot

echo  -e '\033[32mdocker start successfully!... \033[0m'
#---------------------------------------------------------------------------------------------------
#ע��
#������������ӣ�java -jar -Dproperty.config.location=/common.properties /tmp/paybay-dms-1.0.0.jar --spring.config.location=/application.properties