#!/usr/bin/expect
# Change a login shell to tcsh
set timeout 8
set spwan_argv_port [lindex $argv 0] 
set spwan_argv_boxname [lindex $argv 1]
set spwan_argv_boxid [lindex $argv 2]
spawn bash ok ${spwan_argv_port} ${spwan_argv_boxname} ${spwan_argv_boxid} 
expect "(yes/no)?"
send "yes\r"
expect "word:"
send "ubox\r" 
expect "word:"
send "ubox\r" 
expect eof    
exit