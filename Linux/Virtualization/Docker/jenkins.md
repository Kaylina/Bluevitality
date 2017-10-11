### 下载
```Bash
docker pull jenkins:2.60.2
```
### 测试
```Bash
docker run -p 8080:8080 -p 50000:50000 docker.io/jenkins:2.60.2 
```
### dockerfile
```Bash
FROM docker.io/jenkins:2.60.2
ENV TZ=Asia/Shanghai
VOLUME /var/jenkins_home
EXPOSE 8080
EXPOSE 5000
ENTRYPOINT ["/bin/tini", "--", "/usr/local/bin/jenkins.sh"]
```
### 构建镜像
```Bash
docker build -t "paybay_jenkins" .
```
### 随系统自启动本容器
```Bash
docker run -d --restart=always --name jenkins -p 8080:8080 -p 50000:50000 paybay_jenkins
```
### 查找挂载点
```Bash
docker inspect -f {{.Mounts}} instance1
```

[官方镜像](https://github.com/jenkinsci/docker/blob/15dc59d7dbd47da5259a50a9ebfa8895d594444f/Dockerfile)
