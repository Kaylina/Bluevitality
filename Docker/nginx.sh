#!/bin/bash
#ʹ�õĹٷ�nginx���񣬽����������ԴΪ�����ƺ�ִ�С� ��������docker.io/nginx:latest
#���ڱ��ű���ǰĿ¼�ṩnginx�������ļ���web��ԴĿ¼
#������������������"/usr/local/nginx/sharefile"������tomcat���������У�Ҳ��Ҫ���أ�д����Դ...

#����
        image_name=nginx_serv                                   #�����ľ�������
        container_name=nginx                                    #��������������
        container_dir=/usr/local/nginx/sharefile                #����Ҫ��¶��Ŀ¼�������Դ�������ڻᴴ����
        host_dir=/data/nginx/sharefile                          #������¶��Ŀ¼���������еĹ���λ�ã������ڻᴴ����

        
#ɾ���Ѵ����������͹����ľ���
docker rm -f $( docker ps -a | awk /${container_name}/'{print $1}' ) 2> /dev/null
docker rmi $(docker images | awk /${image_name}/'{print $3}' ) 2> /dev/null

#���������ļ���web��Դ
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