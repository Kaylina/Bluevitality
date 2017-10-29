1. `#!` 告诉系统脚本需要什么解释器来执行,一般的有 `#!/bin/ash` 和 `#!/bin/sh`；
2. `./x.sh` 不能写成 `x.sh` ,后者代表到PATH中寻找x.sh文件并执行；
3. 可以直接作为解释器的参数运行shell脚本： `/bin/sh sample.sh`;
4. `#` 为单行注释标记；没有多行注释，可以用函数`{}`代替；一行可执行多条命令，使用引号分隔；
5. 定义变量时不用`$`符号,等号和变量之间不能有空格；
6. 使用变量时要使用`$`符号,同时可以加花括号以识别边界： `echo $name`, `echo ${name}`;
7. `readonly`关键字定义只读变量；`unset`关键字删除变量(只读除外);
8. 运行shell脚本时存在三种变量：局部变量、环境变量、shell变量;
9. shell中的特殊变量：
      $0	当前脚本的文件名
      $n	传递给脚本或函数的参数。n 是一个数字，表示第几个参数。例如，第一个参数是$1，第二个参数是$2。
      $#	传递给脚本或函数的参数个数。
      $*	传递给脚本或函数的所有参数。
      $@	传递给脚本或函数的所有参数。被双引号(" ")包含时，与 $* 稍有不同。
      $?	上个命令的退出状态，或函数的返回值。
      $$	当前Shell进程ID。对于 Shell 脚本，就是这些脚本所在的进程ID。
10. 当被双引号(" ")包含时，"$*" 会将所有的参数作为一个整体，以"$1 $2 … $n"的形式输出所有参数；
    "$@" 会将各个参数分开，以"$1" "$2" … "$n" 的形式输出所有参数。
11. 在使用表达式时添加 `-e` 参数进行特殊字符替换，不加则不替换。如： `echo -e "换行\n"`;
    `-E` 参数为禁止替换(默认); `-n` 参数禁止插入换行符；
12. 命令替换：使用反引号将命令执行结果存储起来。如： DATE=`date;uptime`;echo $DATE
13. 变量替换(预先定义变量在条件下的值)：
      ${var}		变量本来的值
      ${var:-word}	如果变量 var 为空或已被删除(unset)，那么返回 word，但不改变 var 的值。
      ${var:=word}	如果变量 var 为空或已被删除(unset)，那么返回 word，并将 var 的值设置为 word。
      ${var:?message}	如果变量 var 为空或已被删除(unset)，那么将消息 message 送到标准错误输出，可以用来检测
			变量 var 是否可以被正常赋值。若此替换出现在Shell脚本中，那么脚本将停止运行。
      ${var:+word}	如果变量 var 被定义，那么返回 word，但不改变 var 的值。
14. 使用expr进行算术运算，表达式和运算符之间必须有空格： a=10;b=20;echo "a+b=`expr $a + $b`";
    乘法运算必须加反斜杠：`expr $a \* $b`;
      +		加法
      -		减法
      *		乘法
      /		除法
      %		取余
      =		赋值；相等
      !=	不相等	[ $a != $b ] 返回 true。
15. 除了赋值以外，其他算术运算表达式和运算符之间都必须空格；
16. 整数比较：
      -eq	==
      -ne	！=
      -gt	>
      -lt	<
      -ge	>=
      -le	<=
17. 布尔运算符：
      !		非
      -o	或
      -a	且
18. 字符串比较：
      =		和 `==` 类似，但有差别
      =~	前者包含后者(子字符串)
      !=	不等于
      <		ASCII小于
      >		ASCII大于
      -z	为空
      -n	不为空
19. 文件判定：
      -e 	文件或目录存在
      -r	可读
      -w	可写
      -x	可执行
      -s	内容不为空
      -d	目录
      -f	普通文件
      -g	设置了SGID位
      -u	设置了SUID位
      -k	设置了粘着位
      -b	块设备文件
      -c	字符设备文件
20. 单引号字符串内不能使用单引号(转义也不行)，且不会被解析；双引号内可以使用转义字符和变量；
21. 字符串拼接直接写到一起即可(不需要空格)：a="ab";b="cd";c=$a$b;echo "$c";
22. 获取字符串长度：string="abcde";echo ${#string};
23. 提取子字符串：string="abcdefghi";
		  :	指定截取开始位置和截取位数
		 
	注：%%和##从左/右边开始匹配，获取左/右边字符串,%和#与之对应方向相反
		  

24. 查找字符串：string="abcdefghi";echo `expr index "$string" def`;
25. 定义数组：array_name=(value0 value1 value2 ...)
    或者      array_name=(
	      value0
	      value1
	      value2
	      ...
	      )
    或	      ARRAY_NAME[index]=value
26. 读取数组元素：${array_name[index]}
    读取所有数组元素：	${array_name[*]} 或者 ${array_name[@]}
    获取数组长度：${#array_name[@]}
		  ${#array_name[*]}
		  ${#array_name[index]}
27. 双引号可有可无，单引号主要用在原样输出中；
28. echo的结果可以重定向至文件：echo "file contents" > file.txt;
29. shell支持printf命令，用法与C语言有少许差异：printf "%9.3f\n%8.3s\n%9d\n" 1.3 abcdefg 123456;
30. if...else语句：
      if [ expression ]; then
	statements
      elif [ expression ]; then
	statements
      else
	statements
      fi
      也可以写成一行：if test expression;then statements;elif[ expression ];then statements;else statements;fi;
      if :是特殊的空条件，始终返回true;
      注意条件表达式与方括号之间必须有空格，否则语法错误；
31. 普通语句中可以使用 `||` 和 `&&` 符号，但条件表达式中不可以使用，只能用 `-o` 和 `-a`；
32. test命令检查某个条件是否为真，与方括号[]作用相同;
33. case...esac分支：
      case 值 in
      匹配1)
	  command1
	  command2
	  command3
	  ;;
     匹配2)
	  command1
	  command2
	  command3
	  ;;
      *)
	  command1
	  command2
	  command3
	  ;;
      esac
      这里的匹配模式可以使用正则表达式，支持的字符有
		 *       任意字串
                 ?       任意字元
                 [abc]   a, b, 或c三字元其中之一
                 [a-n]   从a到n的任一字元
                 |       多重选择
34. for...in循环：
      for 变量 in 列表
      do
	  command1
	  command2
	  ...
	  commandN
      done
      列表可以是一个字符串，也可以是一组值的序列(通过空格分隔),还可以是文件或目录的集合;
      for FILE in $HOME/.bash*
      do
	echo $FILE
      done
35. while循环：
      while [ expression ];do
	  statements
      done
36. until循环(类似while循环，只不过条件是否定的)：      
      until [ expression ];do 
	  statements
      done
      简洁写法：
	until((i>20));do echo $i;((i++));done
37. 双括号语法：
      语法：
	((表达式1,表达式2...))
      特点：
	1、在双括号结构中，所有表达式可以像c语言一样，如：a++,b--等。
	2、在双括号结构中，所有变量可以不加入：“$”符号前缀。
	3、双括号可以进行逻辑运算，四则运算
	4、双括号结构 扩展了for，while,if条件测试运算
	5、支持多个表达式运算，各个表达式之间用“，”分开
	6、双括号结构之间支持多个表达式，然后加减乘除等c语言常用运算符都支持。如果双括号带：$，将获得表达式值，赋值给左边变量
	7、计算时 `(())` 语法比let、expr更有效率。
      例： a=1;b=2;c=3;a=$((a+1,b++,c++));echo $a;  #结果为2,3,4
38. seq生成序列：
      seq LAST  =>  1 2 3 4 ... LAST
      seq FIRST LAST  =>  FIRST FIRST+1 FIRST+2 ... LAST
      seq FIRST STEP LAST  =>  FIRST FIRST+STEP FIRST+STEP+STEP ... LAST
39. let命令省略引用变量的 `$` 符号并进行数学运算：let sum=sum+1;
40. shell命令，可以按照分号分割，也可以按照换行符分割。如果想一行写入多个命令，可以通过“';”分割;
41. break跳出循环：
      break 默认跳出所有循环
      break n 指定跳出第n层循环
42. continue跳过循环：
      continue 默认跳过当前(最里层)循环
      continue n 指定跳出第n层循环
43. shell函数： 
      function func_name(){
	statements
	return value
      }
      function关键字可以不写，可以没有返回值；
      调用函数只需要写函数名和参数，在函数内部获取参数：
	$n      第n个参数
	$*或$@  所有参数
	$#	参数个数
	$?	函数返回值，在调用函数后获得
      删除函数也可以使用unset，不过要加参数：`unset .f func_name`;
      在~/.profile文件中的函数可以从终端直接调用；
44. 重定向：
      输出重定向：
	command > file   直接覆盖写入，文件不存在则创建
	command >> file	 追加到文件末尾
      输入重定向：
	command < file	 
      例：
	cat > catfile < test.sh  #cat从test.sh 获得输入数据，然后输出给文件catfile
	cat > catfile << eof	 #向cat输入文件结束符，cat输出到catfile，这时不用按ctrl+d即可退出
    深入理解：
      一般情况下，每个 Unix/Linux 命令运行时都会打开三个文件：
	  标准输入文件(stdin)：stdin的文件描述符为0，Unix程序默认从stdin读取数据
	  标准输出文件(stdout)：stdout 的文件描述符为1，Unix程序默认向stdout输出数据
	  标准错误文件(stderr)：stderr的文件描述符为2，Unix程序会向stderr流中写入错误信息
      可用的重定向命令：
      command > file	将输出以覆盖的方式重定向到 file
      command < file	将输入重定向到 file
      command >> file	将输出以追加的方式重定向到 file
      n > file		将文件描述符 n 重定向到 file
      n >> file		将文件描述符 n 以追加的方式重定向到 file
      n >& m		将输出 m 和 n 合并
      n <& m		将输入 m 和 n 合并
      &>file		将标准输出和标准错误输出都重定向file
      << tag		将开始标记 tag 和结束标记 tag 之间的内容作为输入
   注：/dev/null是一个"黑洞"，任何向他写入的内容都被丢弃，也无法从此文件读取到任何内容
45. Here Document:
	command << delimiter
	    document        
	delimiter
    将两个定界符之间的内容作为输入传递给command,与php的定界符类似；
    例：
	vi t.txt <<EndOfCommands
	i
	This file was created automatically from
	a shell script
	^[
	ZZ
	EndOfCommands
     通过vi编辑器将docunemt保存到t.txt文件中
46. 包含文件：
	通过
	    . filename
	或
	    source filename
	来在一个脚本文件中包含一个外部脚本，被包含脚本不必有可执行权限

附 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
脚本内直接定义函数则一旦退出shell则定义将失效。可将其定义在Shell每次启动时重新载入的位置：如.bashrc，并用source或点操作符引用
shell中的函数虽然可通过return返回，但这里的return相当于exit，只能是个状态值用于测试而不能像其它语言一样返回复杂的结果
其处理结果只能通过输出到标准输出经过 `` 
$()取得eval是对Bash Shell命令行处理规则的灵活应用，进而构造"智能"命令实现复杂的功能。
在SHELL的函数中默认使用脚本的全局变量，若需要定义函数内部命名空间的变量需要使用关键字：local

for的形式多种多样：

	for var  in  value1  value2  value3		支持任何可迭代的命令，如：seq 10   或：ls -l   或：echo 1 2 3
	for  i  in   {n..m}				{} 可表示Items： a{1,2} 相当于 a1 a2   {1,2,3} 相当于 {1..3}
	for (( int i = 0 ; i < 10 ; i++ ))		标准C语言格式。((b=102)) 等于let b=102   <----	算术运算（不加$符）
	for i in `*.jpg`		

按行读取文件：
	While read LINE ; do ..... ; done < $Filename
	for line in `cat file ; do ...... ; done
	cat file | while read line ; do ...... ; done
		
	
0为真！（未初始化或者初始化了赋null值则为false，“if COMMAND”结构将返回COMMAND的退出码）
if [ 0 ]
then
    echo "0 is true."
else
    echo "0 is false."
fi


LIMIT=10
for ((a=1; a<=LIMIT; a++))	#LIMIT没有使用$，在((....))中变量的$符号可省略
do
    echo $a
done

动态生成数组：

	start=0;
	total=0;
	for i in $(seq $start 2 1000); do
		total=$(($total+$i));
	done;

Linux系统快捷键：
	ctrl + a | e		行首/行尾
	ctrl + u | k		删到行首/行尾
	ctrl + c | d		终止/输入结束
	ctrl + m	 	回车
	ctrl + z		后台暂停（使用 jobs -l 查看）
	ctrl + l		清屏
	ctrl + z		转入后台运行
	ctrl + s		刷屏信息过快，可用来停留在当前屏
	ctrl + q		恢复刷屏
	
	Pg / Up	 		翻屏
	Alt + c	 		改为大写
	Alt + u	 		全部大写 
	Alt + l  	 	全部小写
	Shift+alt+F1-F6		切换窗口

fock炸弹：
	:(){:|:&;};

sysctl：
	-a		显示系统核心设置
	-w 		设置环境变量，如：sysctl -w net.ipv4.tcp_max_syn_backlog=256
	-p		使配置生效

batch：			在系统平均负载量降到0.8以下时执行某项一次性任务
	#batch 
	at> echo 1234	
	at> <EOT>
	
记录操作：
	scrtipt -a <input-record.log>		开始记录，并指定记录位置
	...........
	.............
	exit					退出记录
	

直接运行：bash script.sh or . script.sh	
在当前Shell运行：source script.sh		
赋予权限运行：	chmod a+x script.sh ; . /script.sh
脚本加密：gzexe Filename		将生成脚本乱码文件，源文件加后缀"~"
语法检查：bash -t  Filename		执行并输出执行过程：bash -x Filename

在当前脚本内引入其他脚本文件：
	.  /path/filename		注：常用于载入已定义好的Shell函数功能模块
	source  /path/filename
	

function name() {
	...........		当发现$(cmd)结构便将cmd执行得到其标准输出，再将此输出放到原命令
	local var=value		local关键字定义函数内的局部变量
	return 0;		其返回值不能通过$?引用，但可以使用$()形式获得！
}
result=`functionname` ; echo ${result}
	

mktemp		创建临时文件
mktemp -d	创建临时目录
	
[[ $Var =~ [[:space:]]* ]]	当使用正则匹配时需要用"=~"符号( 字符串的比较最好使用双中括号!）	
	
timeout运行指定命令，若在指定时间后仍在运行则杀死该进程：
	timeout 10 top    10秒后结束top命令（在shell脚本中比较有用）

uname：
	-a		所有信息
	-m		硬件平台		x86_64
	-n		DNS中的主机名	localhost.localdomain
	-r		内核版本		2.6.32-431.el6.x86_64


trap是Shell内建命令，用于在脚本中指定信号如何处理：
	trap -p 		将当前的trap设置打印出来。
	trap -l			打印所有信号
	trap "cmd" signals	当接收到指定信号时执行指定命令
	trap signals		若没有明亮部分则默认将信号处理复原，如：trap INT 即恢复Ctrl+C退出
	trap "" signals		忽略信号signals，可多个，如：trap "" INT 表明忽略SIGINT信号，按Ctrl+C也不能使脚本退出
	trap "cmd" EXIT		脚本退出时执行cmd
	trap "cmd" ERR		当命令出错，退出码非0，执行cmd
	trap "cmd" RETURN	当从shell函数返回、或用source执行另一脚本文件时，执行commands
	信号：
	trap -l
	1) SIGHUP       	2) SIGINT       	3) SIGQUIT      	4) SIGILL       	5) SIGTRAP
	6) SIGABRT      	7) SIGBUS       	8) SIGFPE       	9) SIGKILL     		10) SIGUSR1
	11) SIGSEGV     	12) SIGUSR2     	13) SIGPIPE     	14) SIGALRM     	15) SIGTERM
	16) SIGSTKFLT   	17) SIGCHLD     	18) SIGCONT     	19) SIGSTOP     	20) SIGTSTP
	21) SIGTTIN     	22) SIGTTOU     	23) SIGURG      	24) SIGXCPU     	25) SIGXFSZ
	26) SIGVTALRM   	27) SIGPROF     	28) SIGWINCH    	29) SIGIO       	30) SIGPWR
	31) SIGSYS      	34) SIGRTMIN    	35) SIGRTMIN+1  	36) SIGRTMIN+2  	37) SIGRTMIN+3
	38) SIGRTMIN+4  	39) SIGRTMIN+5  	40) SIGRTMIN+6  	41) SIGRTMIN+7  	42) SIGRTMIN+8
	43) SIGRTMIN+9  	44) SIGRTMIN+10 	45) SIGRTMIN+11 	46) SIGRTMIN+12 	47) SIGRTMIN+13
	48) SIGRTMIN+14 	49) SIGRTMIN+15 	50) SIGRTMAX-14 	51) SIGRTMAX-13 	52) SIGRTMAX-12
	53) SIGRTMAX-11 	54) SIGRTMAX-10 	55) SIGRTMAX-9  	56) SIGRTMAX-8  	57) SIGRTMAX-7
	58) SIGRTMAX-6  	59) SIGRTMAX-5  	60) SIGRTMAX-4  	61) SIGRTMAX-3  	62) SIGRTMAX-2
	63) SIGRTMAX-1  	64) SIGRTMAX


检查远程端口是否对bash开放：	echo >/dev/tcp/8.8.8.8/53 && echo "open"
让进程转入后台：	Ctrl + z
将进程转到前台：	fg
产生随机的十六进制数，其中n是字符数：	openssl rand -hex n
SSH with pem key:		ssh user@ip_address -i key.pem
用wget抓取完整的网站目录结构，存放到本地目录：	wget -r --no-parent --reject "index.html*" http://hostname/ -P /data
创建 war 文件:		jar -cvf name.war file
测试硬盘写入速度：	dd if=/dev/zero of=/tmp/output.img bs=8k count=256k; rm -rf /tmp/output.img
测试硬盘读取速度：	hdparm -Tt /dev/sda
获取文本的md5 hash：	echo -n "text" | md5sum
检查xml格式：	xmllint --noout file.xml
将tar.gz提取到新目录里：	tar zxvf package.tar.gz -C new_dir
用wget命令执行ftp下载：	wget -m ftp://username:password@hostname
访问Windows共享目录：	smbclient -U "DOMAIN\user" //dc.domain.com/share/test/dir
执行历史记录里的命令(这里是第100行):
qcow2镜像文件转换：	qemu-img convert -f qcow2 -O raw precise-server-amd64-disk1.img \precise-server-amd64-disk1.raw
重复运行文件，显示其输出（缺省是2秒一次）：	watch ps -ef
所有用户列表：	getent passwd
创建临时RAM文件系统 – ramdisk (先创建/tmpram目录):		mount -t tmpfs tmpfs /tmpram -o size=512m
扫描网络寻找开放的端口：	nmap -p 8081 172.20.0.0/16
将文件按行并列显示：	paste test.txt test1.txt
使用curl获取HTTP status code:		curl -sL -w "%{http_code}\\n" www.example.com -o /dev/null
获取文件owner:		stat -c %U file.txt
block设备列表：		lsblk -f

参考自：
http://izualzhy.cn/bash/2015/04/18/advanced-bash-scripting-guide-booknote
http://www.jb51.net/article/52392.htm


