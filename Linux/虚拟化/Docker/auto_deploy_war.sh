#!/bin/bash
#war包全自动部署脚本(非热部署)
#by inmoonlight@163.com

#脚本第一个参数是war包的名字，本脚本必须与war在同一目录下（格式：automatic_deployment_war.sh JAVA.war）
war_full_path="$(pwd -P)/$1"

#判断是否输入了war包的名字
if [[ ! -n "$1" ]] || [[ ! -e "$(pwd -P)/$1" ]] ;then
        echo "you have not input war fiilename!"
        exit 1
fi

#tomcat启动与关闭的脚本路径及webapps路径
tom_up=/usr/local/tomcat/bin/startup.sh
tom_down=/usr/local/tomcat/bin/shutdown.sh
tom_webapps=/usr/local/tomcat/webapps

#关闭tom
function stop() {
        eval "$tom_down"
        sleep 1
        #eval "$tom_down"
        killall java    #慎用 (避免对其他java应用产生影响)
}

#部署war包
function deploy() {
        #按时间创建临时的旧包备份文件
        mkdir -p /tmp/$(date "+%F_%H:%M") || echo "created backup directory fail..."
        cp "${tom_webapps}/${1}" /tmp/$(date "+%F_%H:%M")  &> /dev/null || echo "The file does not exist, the first deployment : $1"
        #移除webapps下的旧包之后再部署
        rm -rf "${tom_webapps}/${1}" "${tom_webapps}/${1%%\.war}" || echo "mv old file fail..."
        mv "${war_full_path}" ${tom_webapps} && echo "Successful deployment..."
}

#启动tom
function start() {
        eval "$tom_up"
}

#run
stop
deploy $1 #传参 (war包名)
start
