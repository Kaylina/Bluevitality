* haresources 资源相关
* ha.cf 心跳设置
* authkeys 认证

在备份节点上也需安装Heartbeat，安装方式与在主节点安装过程一样  
依次安装libnet和heartbeat源码包，安装完毕后在备份节点使用scp命令把主节点配置文件传输到备份节点  

[root@node2 ~]#`scp -r node1:/etc/ha.d/*  /etc/ha.d/`   
