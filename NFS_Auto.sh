#!/bin/bash
#NFS服务C、S端自动安装配置脚本，兼容Centos6、7系列...
#选项：1 服务端设置、2 客户端挂载、3、客户端恢复

#serv_define
	pub_path=/data/nginx/sharefile		#S端共享目录
	net_addr=*				#S端允许访问的地址，eg：192.168.10.0/24

#agen_define
	local_path=/mnt				#C端挂载目录
	serv_ip=127.0.0.1			#C端访问地址

function show_and_conf_public() {

	exportfs -a
	echo -e "\033[32mService config success... \033[0m"
	echo -e "\033[32mPublic_dir:  \033[0m"
	showmount -e
	exit 0
	
}
	
function serv_config() {

	setenforce 0
	
	[ -d "${pub_path}" ] || {
		echo >&1  -e "\033[31m${local_path}不存在...请先创建共享目录 :-) ...\033[0m"
		exit 1
	}
	
	chmod 777 -R ${pub_path}
	
	echo "${pub_path} ${net_addr}(rw,sync)" > /etc/exports
	
	[ -x "/usr/bin/systemctl" ] && {
		#Centos 7
		yum -y install nfs-utils rpcbind
		
		systemctl enable {rpcbind,nfs-server,nfs-lock,nfs-idmap}
		systemctl start {rpcbind,nfs-server,nfs-lock,nfs-idmap}
		
		show_and_conf_public	
	}   
	
	rpm -qa | grep -q nfs || yum -y install nfs-utils
	rpm -qa | grep -q rpcbind || yum -y install rpcbind
	
	service rpcbind start
	service nfs start
	
	chkconfig nfs on --level 235
	chkconfig rpcbind on --level 235
	
	show_and_conf_public	
}

function agen_config() {

	setenforce 0
	
	[ -d "${local_path}" ] || {
		echo >&1  -e "\033[31m${local_path}不存在...请先创建挂载目录 :-) ...\033[0m" 
		exit 1
	}
	
	chmod 766 -R ${local_path}
	
	rpm -qa | grep -q nfs || yum -y install nfs-utils
	rpm -qa | grep -q rpcbind || yum -y install rpcbind
	
	mount -t nfs ${serv_ip}:${pub_path} ${local_path}
	
	echo "${serv_ip}:${pub_path} ${local_path} nfs rsize=8192,wsize=8192,timeo=14,_netdev 0 0" >> /etc/fstab
	echo -e "\033[32mAgent config success... \033[0m"
	
	showmount -e ${serv_ip}
	echo -e "\033[32mLocal mount: \033[0m" ${local_path}
	exit 0
}

read -p "how to config? : S(1) or C(2) or umount(3)?" -n 1 -t 5 var

case $var in  
    	1)  echo ; serv_config  				#输入为1时执行服务端设置
    	;;  				
    	2)  echo ; agen_config  				#输入为2时执行客户端挂载
	;;			
	3)	
	echo ; umount ${local_path}				#输入为3时取消客户端挂载
	sed -i "/^${serv_ip}/d" /etc/fstab
    	;;  
esac

