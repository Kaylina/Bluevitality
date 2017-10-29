#!/bin/bash
#by 2017.1.19   QQ:1115188530
#mail:inmoonlight@163.com
#英语单词循环复习脚本

if [[ "$1" == "--help" ]];then
        echo -e "参数1：单词文件名"
        echo -e "参数2：每个单词的停留时间"
        exit 0
fi

#变量：------------------------------------------------------
filename="$1"                           #单词文件名
time=$2                                 #每个单词的停留时间
maxline=$(cat $filename | wc -l)        #单词数量
#------------------------------------------------------------
#是否需将单词追加到input_word：
function input_word()
{
        echo -n -e "\t\t\t"
        read -p "重点单词？请按1：" -n 1 -t ${time:=2} Y_enter
        if [[ "$Y_enter" == "1" ]];then
                 echo ${word} >> ./input_word
        else
                continue
        fi
}

#样式
function style()
{
        echo "---------------------------------------------"
}

#循环每一行单词并输出
function echo_word()
{
        for((line_number=1 ; line_number <= $maxline ; line_number++))
        do
                clear
                TAB='echo -n -e "\n\n\t\t\t\t\t"'
                eval $TAB ; style
                word=`cat $filename | sed -n "${line_number}p"`
                eval $TAB ; echo -e "\033[40;37m ${word} \033[0m"
                eval $TAB ; style
                if [[ "$line_number" == "${maxline}" ]];then
                        clear
                        echo "Finish!"
                        exit 0
                fi
                input_word              #调用了函数input_word
        done
}

#执行
echo_word
