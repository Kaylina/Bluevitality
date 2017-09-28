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
##### 添加配置
```Bash
cat >> docker.cnf <<eof
[mysqld]
skip-host-cache
skip-name-resolve
character-set-server = utf8
collation-server = utf8_general_ci
default_storage_engine = InnoDB
max_connections = 1000
max_connect_errors = 30
eof
```
##### dockerfile
```Bash
FROM docker.io/mysql:5.7
ADD ADD docker.cnf /etc/mysql/conf.d/docker.cnf
ENV MYSQL_ROOT_PASSWORD=paybay123 
ENV MYSQL_DATABASE='signage' MYSQL_USER='remote' MYSQL_USER='paybay123'
EXPOSE 3306
VOLUME /var/lib/mysql
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["mysqld"]
```

##### 制作镜像
```Bash
docker build -t "paybay_mysql:5.7" .
```

## 启动容器
```Bash
docker run -d -p 3306:3306 paybay_mysql:5.7
```

## 查找挂载卷
```Bash
docker inspect -f {{.Mounts}} <container_ID>
```

[镜像官网地址](https://hub.docker.com/_/mysql/)
