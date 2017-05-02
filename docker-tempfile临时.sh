本周目标：
	docker：（全部在基础镜像的基础上使用dockerfile的方式建立镜像）
		#1、建立私有仓库（harbor）：阿里云
		2、分离的容器：（生产用分布式，注意日志和数据的处理）
			tomcat：
				-1、百度：docker的springboot的jar包部署（这种方式不使用tomcat容器）
				-2、单独为王峰和陈夏君按其给的配置部署各自的tomcat镜像
			nginx：考虑与tom分离后容器静态资源的配置（host不是同一台）考虑方案（NFS或rsync+inotify）
			mysql：数据卷考虑用-v或volume方式、设计成兼容主从的方式、可建立从服务器连接主
			#emq：替代nodejs的mqtt、是一个docker包,load即可
			#	需修改配置：
					config文件中认证服务器的地址、为了更灵活考虑在run.sh中使用-e的方式导入地址
					认证使用http方式、指定http服务器的地址
				
		3、合并的容器：nginx-tomcat-mysql （客户体验用，容易变的部分抽离出来使用环境变量导入）
		
	jenkins:
		重点在mevan，还有jenkins与jdk版本间的兼容性
------------------------------------------------------------------------------------------
docker安装：
	环境:centos 7 （安装时需要翻墙）Docker version 1.12.5
	curl -sSL https://get.docker.com/ | sh
	systemctl start docker.service
	systemctl enable docker.service
	systemctl stop iptables.service
	setenforce 0

EMQ环境：
	下载地址：http://emqtt.com/downloads
	官方手册：http://emqtt.com/docs/v2/install.html
	下载并安装emq的docker镜像：
		wget http://emqtt.com/downloads/2070/docker && unzip emqttd-docker-v2.0.7.zip && docker load < emqttd-docker-v2.0.7
	启动并共享端口：
		docker run -d -p 1883:1883  -p 8083:8083 -p 18083:18083 emqttd-docker-v2.0.7
	注：后续操作等王峰
	进入镜像修改配置（生产用dockerfile）：docker -it emqttd-docker-v2.0.7 sh 
	配置文件？/opt/emqttd/etc/emq.conf (推荐用环境变量导入..)
		
		。。。。。。。。。。。。。。。。。
		备忘：dockerfile在实际的基础镜像基础上建立后，再次建立的仍会跑起来服务！建议先-d跑起来服务之后：docker exec -it 2f01 sh
		
	
私有仓库：
	pip install docker-compose 或：curl -L https://github.com/docker/compose/releases/download/1.8.0/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose #注（docker-compose已经下载好，直接放到/usr/local/bin下并给予执行权限）
	harbor下载地址：https://github.com/vmware/harbor/releases （已经下载了0.5.0版本）
	解压下载的harbor：
		tar -zxvf harbor-offline-installer-0.5.0.tgz
	进入：cd harbor
	修改：
		vim harbor.cfg 注意，生产环境要严格设置其他选项
		hostname = 192.168.126.135
		ui_url_protocol = http
		verify_remote_cert = off
		customize_crt = off
		
	服务端安装harbor
		[root@localhost harbor]#./install.sh
	服务端启动或重启：
		[root@localhost harbor]# docker-compose start/restart


	如果使用的是HTTP方式则docker客户端要修改：
	vim /etc/sysconfig/docker
	#此步骤省略，使用下面的DOCKER_OPTS="$DOCKER_OPTS --insecure-registry <仓库的IP地址>"
	INSECURE_REGISTRY='--insecure-registry <仓库的IP地址>'
	
	
	在客户端重启：（重启服务器后才好）
	systemctl restart docker.service


	客户端登录仓库：
		docker login -u admin -p Harbor12345 <仓库地址>
		
	上传镜像：（注意，仓库地址后面不要加端口号）
		docker tag <镜像名称>  <仓库地址>/<仓库名称>/<镜像名称>:<标签>
		docker push  <仓库地址>/<仓库名称>/<镜像名称>:<标签>

	
	拉取镜像：
		docker pull <仓库地址>/<仓库名称>/<镜像名称>
















