#### 说明
```bash
# 在awk中如果调用next，那么next之后的命令就不执行了。此行的处理到此结束并开始读取下条记录并操作
# 与next相似，getline也读取下1行数据。
# getline究竟实现什么功能呢？正如其名字"得到行"，但注意得到的并不是当前行，而是当前行的下1行
# 但与next不同的是读取下1行之后，把控制权交给了awk脚本的顶部。但其没改变脚本控制，读取下1行后继续运行当前脚本
# 注：getline执行后，会设置NF，NR，FNR和$0等这些内部变量
# 此外getline也可用来执行命令并得到其输出 eg： awk 'BEGIN{"date"|getline;close("date");print $0}'
# 也可从文件中读取内容 eg：awk '{printf "%s ",$0;getline < "b.txt";print $0}' txt （2个文件的每行都打印在1行）
# 如果找到一条记录则getline返回1,如果到了文件结束(EOF)则返回0,如果错误则返回-1

# 当其左右无重定向符 | or < 时：
# getline作用于当前文件，读入当前文件的第1行给其后跟的变量 var 或$0（无变量）
# 应注意到由于awk在处理getline前已经读入了1行所以getline得到的返回结果是隔行的

# 当其左右有重定向符 | or < 时：
# getline作用于定向输入文件，由于该文件刚打开，并没有被awk读入1行
# 只是getline读入，那么getline返回的是该文件的第一行而不是隔行


#  awk可使用shell的重定向符进行重定向输出，如：
awk '$1=100{print $1 > "output_file"}' file
上式表示如果第1个域值等于100则把它输出到output_file。也可用>>来重定向输出，但不清空文件只做追加

# 输入重定向需用到getline函数。
# getline从标准输入、管道或当前正处理的文件之外的其他输入文件获得输入。
# 它从输入获得下1行内容，并给NF,NR和FNR等内建变量赋值
# 如果得到1条记录，getline返回1，如果到达文件末尾就返回0，如果出现错误，如打开文件失败就返回-1
[root@localhost ~]# awk 'BEGIN{"date"|getline d;split(d,a);print a[2]}'
10月

# getline用法大致可分为三大类（每大类又分两小类），即总共有6种用法。代码如下：
[root@localhost ~]# awk ‘BEGIN{“cat data.txt”|getline d; print d}’ data2.txt
[root@localhost ~]# awk ‘BEGIN{“cat data.txt”|getline; print $0}’ data2.txt     #$0可以省略
[root@localhost ~]# awk ‘BEGIN{getline d < “data.txt”; print d}’ data2.txt
[root@localhost ~]# awk ‘BEGIN{getline < “data.txt”; print $0}’ data2.txt       #此种方法不成立
# 以上四行代码均实现“只打印data.txt文件的第一行”（若打印全部行，用循环）


# getline接收用户输入有2种形式：
getline string  < "/dev/tty"
getline string  < "-"
# 提示用户输入参数： 
[root@localhost ~]# awk 'BEGIN{print "input";getline v <"-" ; print v}'  #"-"是标准输入，很多工具都支持
# 获取awk位置参数： 
[root@localhost ~]# awk 'BEGIN{print ARGV[1],ARGV[2]}' a b

# 保存shell的全部输出：
[root@localhost ~]# awk 'BEGIN{srs=RS;RS="" ; "ls ./" | getline TMP ; RS=srs ; print TMP }'

# 使getline直接读取文件
[root@localhost ~]# awk 'BEGIN{ while ( getline d < "aa" ) print d}'
# 注意BEGIN是预处理部分，不是action部分
# 此时还没有准备处理文件，指针也没有指向文件第1行，在执行过程中也不会移动文件指针
# 简单的说就是BEGIN部分awk没有指针，此时只有getline指针，awk只在{ }action部分有指针处理

# 如果getline直接读一个文件，那么就是逐行读取的：
[root@localhost ~]# seq 10|awk '{getline d<"aa";print d}'   
# 因为此时只有getline指针，而没有awk指针来处理该文件

# getline打印偶数行：
[root@localhost ~]# seq 10 | awk 'i++%2'
[root@localhost ~]# seq 10 | awk '{getline;print}' 
# 注意和 seq 10|awk 'BEGIN{while(getline)print}' 区别！BEGIN部分awk没有指针只有getline指针，awk只在{ }action有

# 通过在awk内使用管道,可以把shell命令的输出传送给awk：
[root@localhost ~]# awk 'BEGIN{ "date" | getline d; print d; }'      
2017年 10月 30日 星期一 06:19:13 CST

# system的调用形式是system(cmd).system的返回值是cmd的退出状态.如果要获得cmd的输出,就要和getline结合使用
[root@localhost ~]# awk 'BEGIN{ while( system("ls -l") | getline line ){ print line }}'
总用量 16
-rw-r--r-- 1 root root  72 10月 30 05:43 1
-rw-r--r-- 1 root root   0 10月 30 05:43 　1
-rw-r--r-- 1 root root  16 10月 29 23:21 11
drwxr-xr-x 2 root root   6 10月 30 01:25 hhh
-rw-r--r-- 1 root root  87 10月 30 01:15 ip

# 要求文件a的每行数据与文件b的相对应的行的值相减，得到其绝对值：
[root@localhost ~]# cat numberA
220 34 50 70
553 556 32 21
11 14 98 33
[root@localhost ~]# cat numberB
10
8
2
[root@localhost ~]# awk '{getline j<"numberB";for(i=1;i<=NF;i++){$i>j?$i=$i-j:$i=j-$i}}1' numberA | column -t
210  24   40  60
545  548  24  13
9    12   96  31
# getline依次按行读取文件b里的值，然后for循环依次和文件a里的每个字段进行比较
# 如果比它大就j-$i，要是比它小就$i-j，保证文件相减都是整数
# 当然更法很多，可判断是否小于0，小于0就负负为正，也可以替换到负号这个符号等等
# 总结的说getline可实现2个文件的同步读取而实现一系列的操作。下面是数组的解法：
[root@localhost ~]# awk 'ARGIND==1{a[FNR]=$1;next}{for(i=1;i<=NF;i++)$i=$i-a[FNR];$0=gensub(/-/,"","g")}1' \
 numberB numberA

# 要求文件a里的数据依次替换文件b中的xxx字样
[root@localhost ~]# cat a
aaa
bbb
ccc
ddd
[root@localhost ~]# cat b
111 xxx
222 xxx
333 xxx
444 xxx
[root@localhost ~]# awk '{getline i<"a"}/xxx/{sub("xxx",i,$2)}1' b
111 aaa
222 bbb
333 ccc
444 ddd
# 再看看数组的用法，数组是awk的灵魂，但是有点耗费资源，特别是数百兆上G文件的时候，它挺费劲
awk 'NR==FNR{a[FNR]=$1;next}/xxx/{++i;$2=a[i]}1' a b
```
