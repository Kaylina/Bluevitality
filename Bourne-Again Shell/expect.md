#!/usr/bin/expect
# Change a login shell to tcsh

#等待超时时间
set timeout 8

#定义变量（从位置参数捕获）
set spwan_argv_port [lindex $argv 0] 
set spwan_argv_boxname [lindex $argv 1]
set spwan_argv_boxid [lindex $argv 2]

#调用"ok"脚本并传递expect的命令行参数执行
spawn bash ok ${spwan_argv_port} ${spwan_argv_boxname} ${spwan_argv_boxid} 

#捕获
expect "(yes/no)?"

#发送
send "yes\r"

expect "word:"
send "ubox\r" 

expect "word:"
send "ubox\r" 

expect eof    
exit
