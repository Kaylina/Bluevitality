#!/bin/bash

#get请求
function get_url() {
        result=`curl -s "http://XX.XX.XX.XX/bicloud/sys/createConnect?port=${Box_port}&boxId=${Box_ID}&deviceId=cw01"`
        if [[ "$?" != "0" ]];then 
                echo -e "\033[41;37m Box_ID连接失败！....... \033[0m"       
        fi
}


count=1

#遍历每个网点盒子
for ubox in `cat ./各银行网点盒子监控列表.txt`
do
        #获取盒子ID及端口
        Box_ID=`echo $ubox | awk -F"###" '{print $1}'`
        Box_port=`echo $ubox | awk -F"###" '{print $2}'`
        Box_name=`echo $ubox | awk -F"###" '{print $3}'`
        echo
        echo "----------------------------------------------------------------------------------------------" 
        echo -e "\033[32m 第${count}个盒子 \033[0m";let count++       
        echo -e "\033[32m 盒子ID: $Box_ID \033[0m"
        echo -e "\033[32m 盒子端口: $Box_port \033[0m"
        echo -e "\033[32m 子名称: $Box_name \033[0m"

        #执行URL请求
        get_url
        sleep 2
        ./auto $Box_port $Box_name $Box_ID
done