#!/usr/bin/expect
# Change a login shell to tcsh

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
#   "yes/no" { send "yes\r" ; exp_continue }  #exp_continue可以继续执行下面的匹配，简单了许多
#   "password:" { send "ubox\r" }
# }

expect "word:"
send "ubox\r" 

expect "word:"
send "ubox\r" 

#执行完成后保持交互状态，把控制权交给控制台，此时即可手工操作了。若没有这一句完成后会退出而不是留在远程终端。 
#interact 



expect eof    
exit
