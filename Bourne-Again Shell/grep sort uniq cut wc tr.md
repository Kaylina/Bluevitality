### grep
```bash
-a	不忽略二进制的数据
-A	显示匹配行及其向下N行：grep -A 3 -F "string..."
-B	显示匹配行及其向上N行
-C	显示匹配行及其上下N行
-e	使用正则搜索
-E	使用扩展正则搜索
-o	仅显示被匹配到的模式内容：grep -o -e "x\{1,2\}.*"
-c	统计输出被匹配行的次数
-d	说明要查找的对象是目录
-r	对目录进行递归式的搜索，效果和指定"-d recurse"相同
-f	从文件中读取要配匹配的模式（统计file2中有而file1中没有的行：grep -vFf file1 file2）
-F	将范本样式视为固定字串（非正则且速度快，相当于"fgrep"。统计两个文件共有的行：grep -Ff file1 file2 ）
-h	仅输出匹配内容而不显示被匹配的文件名
-H	输出匹配的同时也输出被匹配的文件名
-l	输出被匹配的文件的文件名，常用于针对路径的递归搜索：grep针对路径的递归搜索：grep -rl "关键字" .
-L	输出未被匹配的文件名，常用于针对路径的递归搜索(多文件查询：grep -L "str" logs1.log logs2.log)
-i	忽略关键字的大小写差异
-n	显示匹配行的行号
-q	不输出任何信息，仅用于脚本中判断grep匹配的返回状态
-s	不显示错误信息
-v	排除查找，即输出没有被匹配的行
-w或--word-regexp   只显示全字符合的列。
-x或--line-regexp   只显示全列符合的列。
-y   此参数的效果和指定“-i”参数相同。
--color	对匹配进行高亮显示
--exclude	过滤不需要匹配的文件类型
--include	指定匹配的文件类型
```
### sort
```bash
-f  忽略大小写
-b  忽略最前面的空格部分，从第一个可见字符开始比较
-M  以月份的名字来排序，如 JAN, DEC 等等的排序方法
-n  使用纯数字进行排序(默认以文字型态排序)；
-r  反向排序
-u  类似与uniq，相同的排序关键字重复行仅输出一行
-t  指定分隔符，默认[tab] 键分隔
-k  以哪个区间进行排序（数字方式以冒号分隔逆向按第3列的第2和第3个字符排序：sort -t":" -nrk 3.2,3.3 file）
-o  将排序后的结果输出至指定的文件
-c  检查是否已经排序
```

### uniq
```bash
-i  忽略大小写
-c  统计重复次数
-u  仅输出不重复的行（唯一的行）
-f  跳过指定列
-d  仅显示重复出现的行列
-s  忽略比较指定的字符。
-n  前n个字段和每个字段前的空白一起被忽略
```

### cut
```bash
-d  指定域分隔符
-f  指定第几列： cut -d ":" -f 2 filename
-c  取指定字符区间（从第二个字符开始到最后：cut -c 2- ）
-b  取指定字节区间
```

### wc
```bash
-l  仅列出行（不带参数的情况下默认输出：行数 单词数 字符数）
-w  仅列出多少字(英文单字)
-m  多少字符
-c  比特数量
```

### tr
```bash
#tr是单个字符处理程序，用于替换或删除字符串或文件中出现的单个字符
-c  除去列表中的字符，通常配合-d,-s选项
-d  删除列表中的字符，不是转换
-s  删除重复字符，如果标准输入里出现了重复多次的source-char-list里所列的字符，将其浓缩成一个

cat file | tr "abc" "xyz" > new_file    将文件file中出现的”abc”替换成”xyz”
cat file | tr [a-z] [A-z] > new_file    小写转大写
cat file | tr -d "hello" > new_file     删除文件file中出现的”hello”字符
cat file | tr -d "\n\t" > new_file      删除file中出现的换行符和制表符
cat file | tr -s [a-z] > new_file       删除file中重复的小写字符，仅留其1个
```

### read
```bash
#read: 用法:read 
#[-ers] [-a 数组] [-d 分隔符] [-i 缓冲区文字] [-n 读取字符数]
#[-N 读取字符数] [-p 提示符] [-t 超时] [-u 文件描述符] [名称 ...]

[root@localhost ~]# read -p "提示" -t 10 -n 100 -a arry
提示1 2 3 4 5
[root@localhost ~]# echo ${arry[@]}
1 2 3 4 5
```

### cat写入时不展开变量
```
[root@localhost ~]# a=123
[root@localhost ~]# cat <<eof
> echo $a
> 
> eof
echo 123

[root@localhost ~]# cat <<'eof'
> echo $a
> 
> eof
echo $a
```

#### basename & dirname
```bash
[root@localhost modules]# pwd
/etc/sysconfig/modules
[root@localhost modules]# basename `pwd`
modules
[root@localhost modules]# dirname `pwd`    
/etc/sysconfig
```
