#!/usr/bin/expect
# expect是交互性很强的脚本语言，它依赖于tcl，而linux一般不自带tcl，需手动安装
# 从最简单的层次来说，expect的工作方式象个通用化的Chat脚本工具。Chat最早用于UUCP网络内以用来实现计算机之间建立连接时进行特定登录会话的自动化
# expect等待输出中输出特定的字符，通常是一个提示符，然后发送特定的响应
# 下载地址：https://pan.baidu.com/s/1kVyeLt9  提取密码：af9p
# tar -zvxf tcl8.4.11-src.tar.gz && cd tcl8.4.11/unix
# ./configure
# make && make install
# tar -zvxf expect-5.43.0.tar.gz
# cd expect-5.43.0
# ./configure --with-tclinclude=/usr/local/src/tcl8.4.11/generic --with-tclconfig=/usr/local/lib/
# make && make install

#等待超时时间
set timeout 8

#定义变量（从位置参数捕获，如果需要接受从bash传递来的参数则可以用 [lindex $argv n] 的形式获得，n从0开始）
set spwan_argv_port [lindex $argv 0] 
set spwan_argv_boxname [lindex $argv 1]
set spwan_argv_boxid [lindex $argv 2]

#调用"ok"脚本并传递expect的命令行参数执行（spawn是expect环境的内部命令）
spawn bash ok ${spwan_argv_port} ${spwan_argv_boxname} ${spwan_argv_boxid} 

#捕获
expect "(yes/no)?"

#发送（\r是回车：ctl + m）
send "yes\r"

# expect {
#     "*yes/no" { send "yes\r"; exp_continue }  #exp_continue可以继续执行下面的匹配，简单了许多
#     "*password:" { send "$pwd\r"; exp_continue }
#     "Enter file in which to save the key*" { send "\n\r"; exp_continue }
#     "Overwrite*" { send "y\n"; exp_continue }
#     "Enter passphrase (empty for no passphrase):" { send "\n\r"; exp_continue }
#     "Enter same passphrase again:" { send "\n\r" }
# }

expect "word:"
send "ubox\r" 

expect "word:"
send "ubox\r" 

#执行完成后保持交互状态，把控制权交给控制台，此时即可手工操作了。若没有这一句完成后会退出而不是留在远程终端。 
#interact 

expect eof    
exit

# SHELL脚本中调用expect：~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# #!/bin/bash
# passwd='PASSWORD'
# /usr/local/bin/expect <<-EOF
# set time 30
# spawn ssh -p22 root@192.168.1.201
# expect {
# "*yes/no" { send "yes\r"; exp_continue }
# "*password:" { send "$passwd\r" }
# }
# expect "*#"
# send "useradd wangshibo\r"
# expect "*#"
# send "mkdir /opt/test\r"
# expect "*#"
# send "exit\r"
# interact
# expect eof
# EOF
