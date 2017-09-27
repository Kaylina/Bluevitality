#!/bin/bash
#C/S需要网络互通，c/s运行时的输出存放在：/var/log/consul-{server,client}.log
#安装时consul二进制包要与脚本在同一目录！
#默认生成配置文件路径：/etc/consul.d。默认开机自启：写入/etc/rc.local
#查询其他功能时执行"h"选项。


#最后一个重要的部分：模板！！！

#SERVER VARIABLES
	service_number=1					#consul服务端数量(高可用)
	data_path=/var/consul					#数据存放目录
	conf_path=/etc/consul.d					#配置存放目录(服务注册信息&健康检测脚本)
	bind_add=192.168.126.135				#consul只能绑定在1个IP(集群node间通讯)
	dc_name=default						#数据中心命名

#CLIENT VARIABLES
	cluster_node_ip=192.168.126.135				#必须定义(集群中任意节点的IP地址)加入集群..
	client_bind_ip=192.168.126.161				#必须定义(client自身绑定的地址)
	register_serv=web					#服务名称
	register_port=80					#服务端口
	register_tages="/var/www/html"			     	#自定义tag信息(建议用于模板进行配置渲染)
	register_check_interval=10				#健康检查间隔，秒
	register_check_scripts="ping -c 1 127.0.0.1 2>&1"	#脚本/命令的返回值，非0则不健康(此检查对应当前服务，注意json)
        register_check_timeout=5                                #脚本执行超时时间(秒)
        register_check_notes="XXX service check fail"           #脚本检查失败提示信息
	kv_storage_enable="on"					#是否启用键值存储功能：on/off
	kv_storage_serv=${register_serv}			#
	kv_storage_key="123"					#键
	kv_storage_value="321"					#值
	dc_name=${dc_name}					#请保持默认(与服务端在同1个数据中心)
	data_path=${data_path}					#
	conf_path=${conf_path}					#

#TEMPLATE VARIABLES
	enable-template="off"					#是否启用模板功能：on/off (可从命令行选项执行)
	only-out-to-view="yes"					#是否不渲染模板仅输出到屏幕：yes/no
	consul_template=/etc/consul.d/consul_template.templ	#服务模板读入路径(需要事先定义好模板!).....
	confige_file=/etc/nginx/nginx.conf			#服务配置文件输出路径
	template_exec="nginx -s reload"				#执行的命令(如重启服务)

#check user
[ "$(id -u)" != "0" ] && { echo -e "\033[1;31mError: must be root to run this script.\033[0m" ; exit 1 ; }

function consul_install() { 

	[[ -x /usr/local/bin/consul ]] ||  { 
		cp ./consul /usr/local/bin  &&  chmod a+x /usr/local/bin/consul
		mkdir -p ${conf_path}  ${data_path}  &&  rm -rf ${conf_path:=protect"/"}/*  ${data_path:=protect"/"}/*
	}  
	
	[[ -x /usr/local/bin/consul-template ]] || {
		cp ./consul-template /usr/local/bin && chmod a+x /usr/local/bin/consul
		mkdir -p ${consul_template%/*} ${confige_file%/*} && rm -rf ${consul_template%/*}/*
	}
	
} 2>&-

function agent_server() {

	consul_install && echo
	
	read -p "please input agent_server_node_name："  -t 8 node_name	#need：node name......
	[[ "${node_name}" == "" ]] && {
		node_name=${RANDOM:1:4}
		echo -e "\033[32mNode_name Not defined.... Use random numbers ${node_name} \n \033[0m"
	}

	consul_command="consul  \
	agent  \
	-server  \
	-rejoin  \
	-ui \
	-bootstrap-expect ${service_number}  \
	-config-dir=${conf_path:=/etc/consul}  \
	-bind=${bind_add}  \
	-client 0.0.0.0"

	echo 	"{
			\"pid_file\": \"/var/run/consul-server.pid\",
    			\"server\": true,
    			\"datacenter\": \"${dc_name}\",
			\"node_name\": \"${node_name}\",
    			\"data_dir\": \"${data_path:=/var/consul}\",
    			\"log_level\": \"INFO\",
    			\"enable_syslog\": true
		 }"  >  ${conf_path}/server.json
	
	[[ "${service_number}" == "1" ]] && consul_command=$( echo ${consul_command} | sed 's/-bootstrap-expect.../-bootstrap /' )
	
	echo -e "\033[32mRun command: \n${consul_command} \n \033[0m"
	
	sed -i "/consul/d" /etc/rc.local  ;  echo ${consul_command} >> /etc/rc.local
	
	eval "nohup ${consul_command} &> /var/log/consul-server.log & " 
	grep -q [[:digit:]] /var/run/consul-server.pid || {
		echo -e "\033[31mconsul service start fail......\033[0m"
		exit 1
	}
	
} 

#仅使用了脚本检查的方式
function  register_service() {

	echo  "{
			\"pid_file\": \"/var/run/consul-client.pid\",
			\"datacenter\": \"${dc_name}\",
			\"node_name\": \"${node_name}\",
			\"disable_remote_exec\": false,
			\"disable_update_check\": false,
			\"retry_interval\": \"10s\",
			\"enable_syslog\": true,
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
		}"  >  ${conf_path}/client.json		#服务注册&健康检查写到配置目录的json文件 service段包括：server & check

}

function kv_storage() {

	curl -X PUT -d "${kv_storage_value}"  http://localhost:8500/v1/kv/${kv_storage_serv}/${kv_storage_key}  &>  /dev/null
	echo -e "\033[32mKV info :\ncurl -s http://${client_bind_ip}:8500/v1/kv/${kv_storage_serv}/${kv_storage_key} \n\033[0m"
	[ "$?" != "0"] && echo -e "\033[31mkv_storage fail..\033[0m"
	
}

function agent_client() {

	read -p "please input agent_client_node_name："  -t 8 node_name
	[[ "${node_name}" == "" ]] && {
		node_name=${RANDOM:1:4}
		echo -e "\033[32mNode_name Not defined.... Use random numbers ${node_name} \n \033[0m"
	}
	
	consul_command="consul  \
	agent  \
	-ui  \
	-bind=${client_bind_ip}  \
	-data-dir=${data_path}  \
	-config-dir=${conf_path}  \
	-join ${cluster_node_ip}  \
	-client 0.0.0.0  \
	-retry-join ${cluster_node_ip}"
	
	register_service ; echo -e "\033[32mregister_service finish... \n\nRun command: \n${consul_command}  \n \033[0m"
	
	sed -i "/consul.*/d" /etc/rc.local
	
	eval "nohup $consul_command &> /var/log/consul-client.log &" && \
	echo $consul_command >> /etc/rc.local || {
		echo -e "\033[31mconsul client start fail...... \n \033[0m"
		exit 1
	}
	
	sleep 0.2 && [[ "${kv_storage_enable}" == "on" ]] && kv_storage &&  echo -e "\033[32mkv_storage success..\033[0m"
	
}  

function script_variables_check() {

	#SERVER VARIABLES CHECK
	[[ ${service_number} =~ [0-9] ]]  \
	&& [[ ${#data_path} -ge 2 ]]  \
	&& [[ ${#conf_path} -ge 2 ]]  \
	&& [[ ${#dc_name} -ge 0 ]]  \
	&& echo ${bind_add} | grep -Eq "[0-9]{2,}\.[0-9]+\.[0-9]+\.[0-9]+" \
	|| {
		echo -e "\033[31mScript Server variables check fail .... \n \033[0m" ; exit 1
	}	
	
	#CLIENT VARIABLES CHECK
	echo ${cluster_node_ip} | grep -Eq "[0-9]{2,}\.[0-9]+\.[0-9]+\.[0-9]+"  \
	&& echo ${client_bind_ip} | grep -Eq "[0-9]{2,}\.[0-9]+\.[0-9]+\.[0-9]+"  \
	&& echo ${kv_storage_enable} | grep -Eq "on|off" \
	&& echo ${register_check_timeout} | grep -Eq "^[[:digit:]]+$"  \
	&& [[ ${#register_serv} -ge 1  &&  ${#register_port} -ge 2 ]]  \
	&& [[ ${#register_tages} -ge 1  &&  ${#register_check_interval} -ge 1 ]]  \
	&& [[ ${#register_check_scripts} -ge 1  &&  ${#kv_storage_enable} -ge 1 ]]  \
   	|| { 
		echo -e "\033[31mScript Client variables check fail .... \n \033[0m" ; exit 1  
	}
	
	#CHECK KV STORAGE
	if [[ "${kv_storage_enable}" != "on" ]] ; then
		if [["${kv_storage_enable}" != "off"]] ; then
			echo -e "\033[31mScript KV variables check fail .... \n \033[0m" 
			exit 1 
		fi
	fi
	
	#CONSUL TEMPLATE CHECK
	echo "${enable-template}" | grep -Eq "on|off" \
	&& echo "${only-out-to-view}" | grep -Eq "yes|no" \
	&& [[ ${#consul_template} -ge 6 && ${#confige_file} -ge 3 ]] \
	&& [[ ${#template_exec} -ge 2 ]] \
	|| {
		echo -e "\033[31mConsul-Temp.. variables check fail .... \n \033[0m" ; exit 1
	}
	
}

function consul_remove() {

	killall consul consul-template
	sed -i '/consul.*/d'  /etc/rc.local
	rm -rf /usr/local/bin/consul /var/{run,log}/consul_* ${conf_path:=protect} ${data_path:=protect} ${consul_template%/*}
	
} 2>&-

function consul_help() {

        consul_help_var=(
	"check_config"
        "show_members"
        "exec_command"
        "all_services"
	"find_service"
        "nodes_info"
        "serv_reload"
        "delete_key"
        "search_key"
	"add_to_key"
        "quit"
        )

        echo -e "\033[1;32mselect:\033[0m" 

        select v in ${consul_help_var[@]} 
        do 

                [[ ${v} == "serv_reload" ]] && consul reload            					#重读配置：kill -HUP
                [[ ${v} == "show_members" ]] && consul members                    
                [[ ${v} == "nodes_info" ]] && curl -s http://127.0.0.1:8500/v1/catalog/nodes?pretty 	 	#查看节点
                [[ ${v} == "all_services" ]] && curl -s http://127.0.0.1:8500/v1/catalog/services?pretty 	#查询所有服务
                [[ ${v} == "check_config" ]] && consul configtest -config-dir=${conf_path} && echo 'ok'		#检查配置文件.不真正启动agent                                    
                [[ ${v} == "find_service" ]] && {
                	#查询提供某服务的所有节点
                        read -p "service name: ";  curl -s http://127.0.0.1:8500/v1/catalog/service/${REPLY}?pretty       
                } 
		
		[[ ${v} == "exec_command" ]] && {
                        #node or service exec command
                        read -p 'exec on node(n) service(s)?' -n 1 
                        [[ "${REPLY}" == "n" ]] && {
                                read -p "node_name:" exec_node_name ; read -p 'commands:' commands
                                consul exec -node="${exec_node_name}" '${exec_command}'
                        } 
			
                        [[ "${REPLY}" == "s" ]] && {
                                read -p 'serv_name:' exec_serv_name ; read -p 'commands:' commands
                                consul exec -service="${exec_serv_name}" '${exec_command}'
                        }  
                }
		
                [[ ${v} == "delete_key" ]] && { 
			#删除单个key (curl -X DELETE http://127.0.0.1:8500/v1/kv/${REPLY}?recurse)
                        read -p 'Key: ' ;  consul kv delete ${REPLY:?var is null!}
                }  
                
                [[ ${v} == "search_key" ]] && {  
                	#查询单个key (url -s http://127.0.0.1:8500/v1/kv/${REPLY}?pretty)
                        read -p 'Key: ' ;  consul kv get ${REPLY:?var is null!}
                } 
		
		[[ ${v} == "add_to_key" ]] && {
			#新增key/value
			echo -e "\033[32mexample: consul kv put service/key value \033[0m"
			read -p 'key_name：'  key_name ; read -p 'key_value：'  key_value
			consul kv put ${key_name:?var is null!} ${key_value:?var is null!}
		}
                
                [[ ${v} == "quit" ]] && break
        done 

}

function template-exec() {

	consul members | grep -qF "server"  || { 
		echo -e "\033[31mconsul_template start fail...[0m"
		exit 1
	}
	
	exec-command="nohuop consul-template -consul-addr 127.0.0.1:8500 -retry 10s -syslog -log-level=info \
	-template "${consul_template}:/${confige_file}:${template_exec}" &> /var/log/consul-template.log &"
	
	if [[ "${only-out-to-view}" == "yes" ]] ;then
		eval $( echo $exec-command | sed -n 's/&.*/-dry/p' )
	else
		eval $exec-command
	fi
	
	[[ "$?" == "0" ]] && echo -e "\033[32m\nconsul-template start success...\033[0m" || exit 1
}

[[ "${enable-template}" == "on" ]] && template-exec

#First check the variables , after the start.....
script_variables_check && echo -en "\033[1;34mIsnatll(i) Uninstall(u) Server(s) Client(c) More_help(m)：\033[0m"

read -t 8

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
        "q")    consul leave 
        ;;
        "m")    consul_help             #查询...
        ;;
	"t")	template-exec		#模板...
	;;
	*)  	exit 1
	;;
esac

#------------------------------------------------------
#       备忘：
#       指定服务执行命令               	consul exec -service="node_name" "exec_command"
#       指定节点执行命令               	consul exec -node="node_name" "exec_command"
#       查某节点所有服务               	curl http://10.245.6.90:8500/v1/catalog/node/《node>
#       查某节点所有检查          	curl http://10.245.6.90:8500/v1/health/node/<node>
#       查某服务所有检查          	curl http://10.245.6.90:8500/v1/health/checks/<service>
#       查某服务所有节点             	curl http://10.245.6.90:8500/v1/health/service/<service>
#       查某状态所有检查          	curl http://10.245.6.90:8500/v1/health/state/<state>

#	加密：
#	S端生成密钥：consul keygen ----> 执行时c/s均追加参数：consul ..... -encrypt=XXXXXXX

#	模板：
#	{{range service "web"}}		注：第一个range的范围相对于URL，即此相对于：http://127.0.0.1:8500/v1/catalog/services下的内容
#	{{.Name}}:{{.Address}}:{{.Port}} --- {{.Tags}}
#	{{end}}
#	
#	{{ if keyExists "app/beta_active" }}	如果指定的key存在则......
#	.......
#	{{ else }}
#	.......
#	{{ end }}
#
#	{{ range ls "service/redis" }}		环绕key？
#	{{ .Key }}:{{ .Value }}{{ end }}
#
#	{{ range services }}			输出：node01 tag1,tag2,tag3
#	{{ .Name }}: {{ .Tags | join "," }}{{ end }}
#
#	{{ base64Decode "aGVsbG8=" }}		hello
#	{{ base64Encode "hello" }}		aGVsbG8=
#	
#	{{ range services }}
#	{{ range service .Name }}
#	{{ end }}
#	{{ end }}



