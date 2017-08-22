## 下载官方镜像
```Bash
docker pull tomcat:7.0.81-jre7
#地址：https://hub.docker.com/_/tomcat/
```
## 运行&测试
```Bash
docker run -d -p 80:8080 tomcat:7.0.81-jre7
curl localhost:80
```

## 删除所有容器
```Bash
docker rm -f $(docker -aq)
```

## 编写Dcoekrfile
##### Dockerfile
```Bash
FROM docker.io/tomcat:7.0.81-jre7
EXPOSE 8080
VOLUME /usr/local/tomcat/conf /usr/local/tomcat/logs /usr/local/tomcat/webapps
CMD ["catalina.sh", "run"]
```
##### 制作镜像
```Bash
docker build -t "tomcat" .
```
## 启动容器
```Bash
docker run -d --name "instance1" -p 80:8080 paybay_tomcat
```
## 查找
```Bash
docker inspect -f {{.Mounts}} instance1
#根据查找的位置放入war包
```

