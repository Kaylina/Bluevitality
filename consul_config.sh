#!/bin/bash

#服务端定义：
	service_number=1		#服务端数量
	data_path=/var/consul		#数据存放目录
	conf_path=/etc/consul.d		#配置存放目录（服务注册信息&健康检测脚本）
	#获取可对外访问的IP地址（仅在单一网关地址且网卡单一地址的情况下有效）
	bind_add=$(ip a s $(netstat -r | awk '/UG/{print $NF}') | awk -F'[/ ]' '/inet/{print $6}')		#consul只能绑定在一个IP上，这里有点问题
	dc_name=default					#数据中心名字

#客户端定义
	cluster_node_ip=127.0.0.1
	register_serv=web
	register_port=80
	register_tages="my_info"
	register_check_interval=10	#second
	register_check_scripts="curl localhost >/dev/null 2>&1"	#返回值非0则表示不正常
	kv_storage_enable="on"														#是否启用键值存储功能（on/off）
	kv_storage_serv=${register_serv}
	kv_storage_key="123"
	kv_storage_value="321"
	dc_name=${dc_name}		#请保持默认
	data_path=${data_path}		#
	conf_path=${conf_path}		#

function install() {

	cp ./consul /usr/local/bin  &&  chmod a+x /usr/local/bin/consul
	
}

function agent_server() {
	#运行时获取：node name......
	read -p "please input agent_server_node_name："  -t 10 node_name
	[[ "${node_name}" == "" ]] && {  
		echo "need node name..."
		exit 1
	}
	#构造执行命令
	consul_command="consul  \
	agent  \
	-server  \
	-rejoin  \
	-bootstrap-expect ${service_number}  \
	-pid-file=/var/run/consul_server.pid  \
	-datacenter ${dc_name}  \
	-data-dir=${data_path:=/var/consul}  \
	-config-dir=${conf_path:=/etc/consul}  \
	-node=${node_name}  \
	-bind=${bind_add:=0.0.0.0}  \
	-client 0.0.0.0  \
	-syslog"
	#写入自起并执行
	[[ "${service_number}" == "1" ]] && consul_command=$( echo ${consul_command} | sed 's/-bootstrap-expect.../-bootstrap /' )
	
	echo -e "\033[32mRun command: \n ${consul_command}\033[0m"
	
	sed -i "/consul/d" /etc/rc.local
	
	echo ${consul_command} >> /etc/rc.local
	
	eval ${consul_command}  ||  {
		echo -e "\033[31mconsul service start fail......\033[0m"
		exit 1
	}
	
} #2>>  /var/log/consul-server-error.log	#安装错误日志

function  register_service() {

	echo "{
			\"service\": {
				\"check\": {
					\"interval\": \"${register_check_interval}s\",
					\"script\": \"${register_check_scripts}\"
				},
				\"name\": \"${register_serv}\",
				\"port\": ${register_port},
				\"tags\": [
					\"${register_tages:=user_info}\"
				]
			}
		}" > ${conf_path}/${register_serv}.json	#服务注册&健康检查信息写到配置目录，文件格式为：".json"
		
}

function kv_storage() {

	curl -X PUT -d  "${kv_storage_value}" http://localhost:8500/v1/kv/${kv_storage_serv}/${kv_storage_key}
	echo -e "\033[32mabout KV info .... please look over:\ncurl http://localhost:8500/v1/kv/${kv_storage_serv}/${kv_storage_key}\033[0m"
	
}

function agent_client() {

	read -p "please input agent_client_node_name："  -t 10 node_name
	[[ "${node_name}" == "" ]] && {  
		echo "need node name..."
		exit 1
	}
	
	consul_command="consul  \
	agent  \
	-ui  \
	-node=${node_name}  \
	-pid-file=/var/run/consul_client.pid  \
	-bind=0.0.0.0  \
	-datacenter=${dc_name}  \
	-data-dir=${data_path}  \
	-config-dir=${conf_path}  \
	-join ${cluster_node_ip}  \
	-rejoin   \
	-syslog"
	
	register_service ; echo -e "\033[32mRun command: \n ${consul_command}\033[0m"
	
	sed -i "/consul/d" /etc/rc.local
	
	eval $consul_command  && echo $consul_command >> /etc/rc.local  ||  {
		echo -e "\033[31mconsul client start fail......\033[0m"
	}
	
} #2>>  /var/log/consul-client-error.log		#安装错误日志

function serv_help() {

	echo  -e "\033[32m帮助信息，信息说明，变量定义说明....备忘信息.....\033[0m"
	
}

function script_variables_check() {
	#服务端变量检查
	[[ ${service_number} =~ [0-9] ]]  && [[ ${#data_path} > 3 ]]  \
	&& [[ ${#conf_path} > 3 ]] && [[ ${#dc_name} -ge 1 ]]  \
	&& echo ${bind_add} | grep -Eq "[0-9]{2,}\.[0-9]\.[0-9]\.[0-9]" ||  \ 
	{
		echo -e "\033[31mscript Service variables check fail ....\033[0m"
		exit 1
	}	
	#客户端变量检查
	echo ${cluster_node_ip} | grep -Eq "[0-9]{2,}\.[0-9]\.[0-9]\.[0-9]"  \
	&& [[ ${#register_serv} > 1 ]] &&	[[ ${#register_port} -ge 2 ]]  \
	&& [[ ${#register_tages} -ge 1 ]] &&	[[ ${#register_check_interval} -ge 1 ]]  \
	&& [[ ${#register_check_scripts} -ge 1 ]] && 	[[ ${#kv_storage_enable} -ge 1 ]]  \
	&& [[ "${kv_storage_enable}" == "on" || "${kv_storage_enable}" == "off" ]]  ||  \ 
	{ 
		echo -e "\033[31mscript Client variables check fail ....\033[0m" 
		exit 1  
	}
	
	[[ "${kv_storage_enable}" == "on" ]] && {
		[[ ${#kv_storage_key} > 1 ]] && [[ ${#kv_storage_value} > 1 ]]  ||  \
		echo -e "\033[31mscript Client variables check fail ....\033[0m" 
		exit 1 
	}
}

function uninstall() {

	sed -i '/consul.*/d'  /etc/rc.local
	rm -rf /usr/local/bin/consul ${conf_path:?conf_path not define} ${data_path:?data_path not define}
	rm -rf /var/run/consul_server.pid  /var/run/consul_client.pid
	
}

mkdir -p ${conf_path}  ${data_path} 2>/dev/null && rm -rf ${conf_path:1}/*  ${data_path:1}/*

script_variables_check && read -p "isnatll(i)  server(s)  client(c)  uninstall(u)  help(h)：" -n 1 var
case ${var} in 
	"i") 	install
	;;
	"s") 	agent_server
	;;
	"c") 	agent_client
	;;
	"u") uninstall
	;;
	"h") 	serv_help
	;;
	*) 	exit 1
	;;
esac
