#!/bin/bash
#使用的官方nginx镜像，建议更换镜像源为阿里云后执行、 镜像名：docker.io/nginx:latest
#需在本脚本当前目录提供nginx的配置文件、web资源目录
#本例与宿主机共享了"/usr/local/nginx/sharefile"。用于tomcat容器像其中（也需要挂载）写入资源...

#定义
        image_name=nginx_serv                                   #构建的镜像名字
        container_name=nginx                                    #构建的容器名字
        container_dir=/usr/local/nginx/sharefile                #容器要暴露的目录（存放资源，不存在会创建）
        host_dir=/data/nginx/sharefile                          #容器暴露的目录在宿主机中的挂载位置（不存在会创建）

        
#删除已创建的容器和构建的镜像
docker rm -f $( docker ps -a | awk /${container_name}/'{print $1}' ) 2> /dev/null
docker rmi $(docker images | awk /${image_name}/'{print $3}' ) 2> /dev/null

#加入配置文件及web资源
cat > dockerfile <<eof
FROM docker.io/nginx:latest
ADD ./conf /etc/nginx/nginx.conf
ADD ./html /usr/share/nginx/html
VOLUME /var/log/nginx
RUN mkdir -p ${container_dir}
EXPOSE 80
EXPOSE 443
eof

docker build -t "${image_name}" .

mkdir -p ${host_dir} 2> /dev/null

docker run -d  \
--name ${container_name}  \
-p 80:80 \
-v ${host_dir:?var not define}:${container_dir:?var not define}:rw  \
${image_name}

