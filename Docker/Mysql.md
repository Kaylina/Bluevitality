## 下载官方镜像
```Bash
docker pull mysql:5.7
```

## 运行&测试
```Bash
docker run --name "mysql" -p 3306:3306 -e MYSQL_ROOT_PASSWORD=paybay123 -d mysql:5.7
#删除镜像:docker rm -f mysql
```

## 编写Dockerfile
##### dockerfile
```Bash
FROM docker.io/mysql:5.7
ENV MYSQL_ROOT_PASSWORD=paybay123 
ENV MYSQL_DATABASE='signage' MYSQL_USER='remote' MYSQL_USER='paybay123'
ENV CHARACTER_SET_SERVER=utf8 DEFAULT_CHARACTER_SET=utf
EXPOSE 3306
VOLUME /var/lib/mysql
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["mysqld"]
```

##### 制作镜像
```Bash
docker build -t "mysql:5.7" .
```

## 启动容器
```Bash
docker run -d -p 3333:3306 mysql:5.7
```

## 查找挂载卷
```Bash
docker inspect -f {{.Mounts}} <container_ID>
```

[镜像官网地址](https://hub.docker.com/_/mysql/)
