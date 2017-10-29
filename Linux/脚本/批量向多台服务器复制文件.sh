#!/bin/bash

# 脚本要求实现：
# 将本机/etc下以conf为扩展名的文件打包压缩为tar.bz2 然后将此文件复制1份到10.0.100.1-->10.0.100.254地址段上所有开启的主机
# 具体路径为/tmp/sjjy/文件，在使用scp复制时无需手动输入密码

# 环境说明：
# (1) 所有服务器将防火墙和selinux关闭
# (2) 所有服务器的root密码为aixocm
# (3) 所有服务器都为10.0.100.*网段，并保证能够和其它主机通信（需要事先存在nmap软件）
# (4) 所有服务器确保sshd服务已经启动 (默认的22端口)

# 思路说明：
# (1) Tar_etc()：  实现对/etc下所有*.conf目录的打包，并判断是否成功
# (2) Nmap_ip()：  扫描已开启的主机。用nmap实现。并将这些主机IP写到"/mydate/ip.txt"文件
# (3) Scp_ip()：   实现将压缩包发送到各个主机的指定目录下，利用了expect来实现输入

#打包/etc/*.conf下的文件：
function Tar_etc() {
    tar jcvf /tmp/lyj.tar.bz2 /etc/*.conf  &> /dev/null
    if [ $? -eq 0 ]
    then
       echo "压缩包打包完成"
    else
       echo "压缩包打包失败请检查"
       exit 1
    fi  
}

#扫描网段内开启的主机
function Nmap_ip() {
    if [ -f /mydate/ip.txt ]
    then
        : >/mydate/ip.txt
    else
        mkdir /mydate 
        touch /mydate/ip.txt
    fi
  nmap -n -sP 10.0.100.1-254 | awk '/10.0.100/{print $5 >> /mydate/ip.txt }'
}


#复制文件到各个主机
function Scp_ip() {
cat /mydate/ip.txt | while read line
do
  (
     /usr/bin/expect << EOF
     set time 20
     spawn scp /tmp/lyj.tar.bz2 root@$line:/tmp/sjjy
     expect {
          "*yes/no*"
            { send "yes\r";exp_continue }
          "*password:"
            { send "aixocm\r"}
     }
     expect eof
EOF
  ) &>/dev/null
    
     if [ $? -eq 0 ]
     then
         echo "复制文件到 $line 成功！"
     else
         echo "复制文件到 $line 失败！"
         exit 1
     fi
done
}
 
Tar_etc 
Nmap_ip
Scp_ip
