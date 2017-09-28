## 下载
```
docker pull wnameless/oracle-xe-11g
```

## 运行
```
docker run -d -p 49160:22 -p 49161:1521 -e ORACLE_ALLOW_REMOTE=true wnameless/oracle-xe-11g
```

## 连接信息
```
hostname: localhost
port: 49161
sid: xe
username: system
password: oracle
```

[官方镜像地址](https://hub.docker.com/r/fengzhou/docker-weblogic-1036/)
