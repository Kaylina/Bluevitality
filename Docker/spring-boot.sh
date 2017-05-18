#!/bin/bash
#jar包和配置文件需要在当前目录！

#DMS服务需要的端口（不能与已经使用的端口冲突，若修改则war包中EMQ的地址也要修改）
SERV_PORT=8011
#数据库服务的IP地址及账号密码
DB_ADDRESS=139.196.238.XX
#emq服务器地址
EMQ_ADDRESS=139.196.238.xx
#建议保持默认（产生随机数修改ID..）
EMQ_ID=$(echo ${RANDOM} | cut -c 1-2)

#---------------------------------------------------------------------------------------------------
#加载默认镜像（若存在不加载）
docker images | grep -q openjdk || docker load < openjre.8.tar
#删除已经创建的容器和构建的镜像
docker rm -f $(docker ps -a | awk '/paybay-dms-spring-boot/{print $1}' ) 2> /dev/null 
docker rmi $(docker images | awk '/paybay-dms/{print $3}') 2> dev/null

sed -Ei  "1,9s#[0-9]{2,}\.[0-9]+\.[0-9]+\.[0-9]+#${DB_ADDRESS:?var not define}#g" application.properties
sed -Ei  "1,9s#[0-9]{2,}\.[0-9]+\.[0-9]+\.[0-9]+#${EMQ_ADDRESS:?var not define}#g" common.properties
sed -Ei  "s#id=(..........).*#id=\1${EMQ_ID}#" common.properties
echo -e '\033[32mconfiguration modified successfully!... \033[0m' || { echo -e  '\033[31mconfiguration modified fail!... \033[0m' ; exit 1 ; }
#设置dockerfile（加入配置文件&设置启动时执行的命令）
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
#构建镜像：
docker build -t  paybay-dms-spring-boot  .
#启动容器：
docker run -p ${SERV_PORT}:${SERV_PORT} -d  paybay-dms-spring-boot

echo  -e '\033[32mdocker start successfully!... \033[0m'
#---------------------------------------------------------------------------------------------------
#注：
#启动命令的例子：java -jar -Dproperty.config.location=/common.properties /tmp/paybay-dms-1.0.0.jar --spring.config.location=/application.properties
