#!/bin/bash
#C/S需要网络互通，c/s运行时的输出存放在：/var/log/consul-{server,client}.log
#配置文件都在哪里？
#会不会开机自启，写在了哪里？
#如何查询？
#脚本如何写？
#如何使用
#最后一个重要的部分：模板！！！

#目前：
# 删除key要注意先写服务名再写key名！配置检查没提示？exec在Node节点提示被忽略！
# KV注册没有成功....

#SERVER VARIABLES
	service_number=1					#服务端数量
	data_path=/var/consul					#数据存放目录
	conf_path=/etc/consul.d					#配置存放目录（服务注册信息&健康检测脚本）
	bind_add=192.168.10.1					#consul只能绑定在一个IP上
	dc_name=default						#数据中心名字

#CLIENT VARIABLES
	cluster_node_ip=192.168.10.1				#必须定义（集群中任意节点的IP地址）
	client_bind_ip=192.168.10.2				#必须定义（自身绑定的地址）
	register_serv=web					#服务名称
	register_port=80					#服务端口
	register_tages="my_info"				#用户自定义tag信息
	register_check_interval=10				#健康检查间隔，second
	register_check_scripts="ping -c 1 127.0.0.1 2>&1"	#脚本/命令的返回值非0则不健康（此检查对应当前服务，注意json信息）
        register_check_timeout=5                                #脚本执行超时时间（秒）【还没加入变量检查】
        register_check_notes="XXX service check fail"           #脚本检查失败提示信息【还没加入变量检查】
	kv_storage_enable="on"					#是否启用键值存储功能（on/off）
	kv_storage_serv=${register_serv}			#
	kv_storage_key="123"					#键
	kv_storage_value="321"					#值
	dc_name=${dc_name}					#请保持默认（同一个数据中心）
	data_path=${data_path}					#
	conf_path=${conf_path}					#

function consul_install() {

	[[ -e /usr/local/bin/consul ]] ||  {
		cp ./consul /usr/local/bin  &&  chmod a+x /usr/local/bin/consul
	}
	
}

function agent_server() {

	consul_install
	echo
	
	read -p "please input agent_server_node_name："  -t 12 node_name	#need：node name......
	[[ "${node_name}" == "" ]] && {  
		echo -e "\033[32mnode_name Not defined.... Use random numbers\033[0m"
		node_name=${RANDOM:1:4}
	}

	consul_command="consul  \
    	agent  \
    	-server  \
    	-rejoin  \
        -ui \
    	-bootstrap-expect ${service_number}  \
    	-pid-file=/var/run/consul_server.pid  \
    	-datacenter ${dc_name}  \
    	-data-dir=${data_path:=/var/consul}  \
    	-config-dir=${conf_path:=/etc/consul}  \
    	-node=${node_name}  \
    	-bind=${bind_add}  \
    	-client 0.0.0.0  \
    	-syslog"

	[[ "${service_number}" == "1" ]] && consul_command=$( echo ${consul_command} | sed 's/-bootstrap-expect.../-bootstrap /' )
	
	echo -e "\033[32mRun command: \n ${consul_command}\033[0m"
	
	sed -i "/consul/d" /etc/rc.local  ;  echo ${consul_command} >> /etc/rc.local
	
	eval "nohup ${consul_command} &> /var/log/consul-server.log & "  ||  \
	{
		echo -e "\033[31mconsul service start fail......\033[0m"
		exit 1
	}
	
} 

#仅适用了脚本检查的方式
function  register_service() {

	echo "  {
			\"service\": {
				\"check\": {
                                        \"name\": \"service check\",
					\"script\": \"${register_check_scripts}\",
					\"interval\": \"${register_check_interval}s\",
                                        \"timeout\": \"${register_check_timeout:=5}s\",
                                        \"notes\": \"${register_check_notes}\"
				},
				\"name\": \"${register_serv}\",
				\"port\": ${register_port},
				\"tags\": [
					\"${register_tages:=user_info}\"
				]
		}
		}" > ${conf_path}/${register_serv}.json	     #服务注册&健康检查写到配置目录的json文件（service段包括server及其check）
		
}

function kv_storage() {

	curl -X PUT -d  "${kv_storage_value}" http://localhost:8500/v1/kv/${kv_storage_serv}/${kv_storage_key}  &>  /dev/null
	echo -e "\033[32mabout KV info :\ncurl http://${client_bind_ip}:8500/v1/kv/${kv_storage_serv}/${kv_storage_key}\033[0m"
        echo
	
}

function agent_client() {

	read -p "please input agent_client_node_name："  -t 12 node_name
	[[ "${node_name}" == "" ]] && {  
		echo -e "\033[32mnode_name Not defined.... Use random numbers\033[0m"
		node_name=${RANDOM:1:4}
	}
	
	consul_command="consul  \
    	agent  \
    	-ui  \
    	-node=${node_name}  \
    	-pid-file=/var/run/consul_client.pid  \
    	-bind=${client_bind_ip}  \
    	-datacenter=${dc_name}  \
    	-data-dir=${data_path}  \
    	-config-dir=${conf_path}  \
    	-join ${cluster_node_ip}  \
	-client 0.0.0.0  \
    	-rejoin   \
    	-syslog"
	
	register_service  ;  echo -e "\033[32mregister_service finish...\nRun command: \n ${consul_command}\033[0m"
	
	sed -i "/consul/d" /etc/rc.local
	
	eval "nohup $consul_command &> /var/log/consul-client.log &" && \
	echo $consul_command >> /etc/rc.local || {
		echo -e "\033[31mconsul client start fail......\033[0m"
		exit 1
	}
	
	sleep 0.1 && [[ "${kv_storage_enable}" == "on" ]] && kv_storage &&  echo -e "\033[32mkv_storage config success..\033[0m"
	
}  

function script_variables_check() {

	#SERVER VARIABLES CHECK
	[[ ${service_number} =~ [0-9] ]]  \
	&& [[ ${#data_path} -ge 2 ]]  \
	&& [[ ${#conf_path} -ge 2 ]]  \
	&& [[ ${#dc_name} -ge 0 ]]  \
	&& echo ${bind_add} | grep -Eq "[0-9]{2,}\.[0-9]+\.[0-9]+\.[0-9]+" \
	|| {
		echo -e "\033[31mscript Service variables check fail ....\033[0m"
		exit 1
	}	
	
	#CLIENT VARIABLES CHECK
	echo ${cluster_node_ip} | grep -Eq "[0-9]{2,}\.[0-9]+\.[0-9]+\.[0-9]+"  \
	&& echo ${client_bind_ip} | grep -Eq "[0-9]{2,}\.[0-9]+\.[0-9]+\.[0-9]+"  \
	&& [[ ${#register_serv} -ge 1  &&  ${#register_port} -ge 2 ]]  \
	&& [[ ${#register_tages} -ge 1  &&  ${#register_check_interval} -ge 1 ]]  \
	&& [[ ${#register_check_scripts} -ge 1  &&  ${#kv_storage_enable} -ge 1 ]]  \
	&& [[ "${kv_storage_enable}" == "on" || "${kv_storage_enable}" == "off" ]]  \
   	|| { 
		echo -e "\033[31mscript Client variables check fail ....\033[0m" 
		exit 1  
	}
	
	#CHECK KV STORAGE
	if [[ "${kv_storage_enable}" != "on" ]] ; then
		if [["${kv_storage_enable}" != "off"]] ; then
			echo -e "\033[31mscript KV variables check fail ....\033[0m" 
			exit 1 
		fi
	fi
}

function consul_remove() {

	killall consul
	sed -i '/consul.*/d'  /etc/rc.local
	rm -rf /usr/local/bin/consul ${conf_path:=protect"/"} ${data_path:=protect"/"}
	rm -rf /var/run/consul_server.pid  /var/run/consul_client.pid
	
}
function consul_help() {

        consul_help_var=(
        "members"
        "services_info"
        "nodes_info"
        "reload"
        "check_config"
        "delete_key"
        "search_key"
        "about_service's_node.."
        "exec_command"
        quit
        )

        echo -e "\033[32mselect:\033[0m" 

        select v in ${consul_help_var[@]} 
        do 
                [[ ${v} == "members" ]] && { consul members ;}                    
                [[ ${v} == "services_info" ]] && { curl http://127.0.0.1:8500/v1/catalog/services ;}         #查询所有服务
                [[ ${v} == "nodes_info" ]] && { curl http://127.0.0.1:8500/v1/catalog/nodes ;}               #查看节点
                [[ ${v} == "reload" ]] && { consul reload ;}                 #重读配置，相当于：kill -1 或： kill -HUP
                [[ ${v} == "check_config" ]] && { 
                
                        consul configtest -config-dir ${conf_path} #检查配置文件.不真正启动agent。
                }               
                
                [[ ${v} ==  "delete_key" ]] && { 
                
                        read -p "Key: "                 #删除单个key
                        curl -X DELETE http://127.0.0.1:8500/v1/kv/${REPLY}?recurse 
                }  
                
                [[ ${v} == "search_key" ]] && {  
                
                        read -p "Key: "                 #查询单个key
                        curl http://127.0.0.1:8500/v1/kv/${REPLY}
                        
                }                              
                
                [[ ${v} == "about_service's_node.." ]] && {
                
                        read -p "service name: "        #查询提供某服务的所有节点
                        curl http://127.0.0.1:8500/v1/catalog/service/${REPLY}    
                        
                }                             
                
                [[ ${v} == "exec_command" ]] && {
                        #node or service exec command
                        read -p "node(n) server(s)" -n 1 
                        [[ "${REPLY}" == "n" ]] && {
                                read -p "node_name:" exec_node_name
                                read -p "node_exec:" exec_command
                                consul exec -node="${exec_node_name}" '${exec_command}'
                        } 
                        [[ "${REPLY}" == "s" ]] && {
                                read -p "serv_name:" exec_serv_name
                                read -p "serv_exec:" exec_command
                                consul exec -service="${exec_serv_name}" '${exec_command}'
                        }  
                }
                
                [[ ${v} == "quit" ]] && break
        done 

}

mkdir -p ${conf_path}  ${data_path} 2> /dev/null && rm -rf ${conf_path:=protect"/"}/*  ${data_path:=protect"/"}/*

#First check the variables , after the start.....
script_variables_check && read -p "isnatll(i) uninstall(u) server(s) client(c) consul_info(h)：" -t 20 

echo
case ${REPLY} in 
	"i") 	consul_install
	;;
	"u")  	consul_remove
	;;
	"s") 	agent_server
	;;
	"c") 	agent_client
	;;
        "q")    consul leave            #离开集群
        ;;
        "h")    consul_help             #查询...
        ;;
	*)  	exit 1
	;;
esac

#模板：
#	模板要查询的服务端地址
#	模板监控的服务（要提供配置文件，比如Nginx）
#	模板要执行的命令（要考虑到docker环境）
#------------------------------------------------------
#
#如果周末来得及：（先不考虑和consul结合的太紧密的场景，仅使用）
#	docker的swarm集群的初始化环境配置和网络配置
#	注：脚本方式...


#       备忘：
#       指定服务执行命令               consul exec -service="node_name" "exec_command"
#       指定节点执行命令               consul exec -node="node_name" "exec_command"
#       查某节点所有服务               curl http://10.245.6.90:8500/v1/catalog/node/:node
#       查某节点所有Checks           curl http://10.245.6.90:8500/v1/health/node/:node
#       查某服务所有Checks          curl http://10.245.6.90:8500/v1/health/checks/:service
#       查某服务所有节点              curl http://10.245.6.90:8500/v1/health/service/:service
#       查某状态所有Checks          curl http://10.245.6.90:8500/v1/health/state/:state




