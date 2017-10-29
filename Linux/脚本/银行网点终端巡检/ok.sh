#/bin/bash

#格式：script_name ssh_port <1/2>

#定义
ssh_port=$1
Bank_BoxName=$2 #第三个参数为网点盒子名字！
Box_ID=$3
Samba_Path="/home/public/网点盒子监控记录"

#删除存储的公钥认证
rm -rf /root/.ssh/known_hosts

#截图：
function ssh_screencap() {
        echo -e "\033[31m 连接至反向链接服务器，需输入密码：ubox \033[0m"
        ssh root@121.42.15X.X -p ${ssh_port} 'su -c "screencap -p /sdcard/6.png"'
        if [[ "$?" != "0" ]];then
                echo  -e "\033[31m 尝试更换端口重新进行SSH连接！！ \033[0m"
                temp_port=$(($RANDOM%9+1))
                ssh root@XX.XX.XX.XX -p 2222${temp_port} 'su -c "screencap -p /sdcard/6.png"'
        fi
        if [[ "$?" != "0" ]];then
                echo -e "\033[31m SSH连接失败，可能的原因：盒子不在线，或ssh服务不可用..... \033[0m"
                echo -e "`date "+%T"`[ ${Bank_BoxName} \t ${Box_ID} \t SSH连接失败.... ] " >> ${Samba_Path}/Error_log_`date "+%F"`.txt
                chmod 777 /home/public/网点盒子监控记录/Error_log_*
                exit 1
        fi
        sleep 1
}

#传输：
function ssh_transport() {
        echo -e "\033[31m 将截图拷贝到当前目录..... \033[0m"
        if [ -f ./6.png ];then
                rm ./6.png
        fi
        scp -P ${ssh_port} root@XX.XX.XX.XX:/sdcard/6.png  .
        echo -e "\033[31m 将截图传输至samba!................................................................... \033[0m"
        png_Time=`date "+%H"`
        mv ./6.png ${Samba_Path}/${Bank_BoxName}_${ssh_port}_${png_Time}.png
}


cat ./status | grep ok
if [[ "$?" != "0" ]];then
         echo -e "\033[31m                                                                                      上一步操作未成功！......................... \033[0m"
fi

: > ./status

#默认先截图后传输至Samba
ssh_screencap && ssh_transport

#若执行到这里说明以上没问题
echo ok >> ./status
