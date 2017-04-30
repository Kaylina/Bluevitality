#创建环境：
mkdir 1400{1..4}/{digital,poems,phrase} -p
touch 1400{1..4}/digital/SI_devide4_number_{01..15}.wav
touch 1400{1..4}/poems/SI_devide4_number_{16..30}.wav
touch 1400{1..4}/phrase/SI_devide4_number_{31..60}.wav

#--------------------------------------------------------------------------	
#开始修改：

#!/bin/bash
#这个要在数据大文件夹下面执行，比如/数据大文件夹/1400.... 就创建在：数据大文件夹/shell.sh ，然后执行：bash shell.sh

#第一层目录
for n1 in 1400{1..4};
{	    #第二层目录
            for n2 in {digital,poems,phrase};
            {
		     #进入目录后将以SI开头的文件交给awk。以关键字:"_number_"做分隔，变量"li"是当前所在目录名 输出:"mv 原名 新名" 并交给Bash执行
                     cd ${n1}/${n2} &&  ls SI* | awk -F "_number_" -v li="$(basename $(pwd))" '{print "mv " $0 " "  $1 "_" li "_" $2}' | bash -
		     #执行完后返回脚本所在目录（在"数据大文件夹"这个目录下执行）
                     cd ../..
            }
}



#--------------------------------------------------------------------------
#复制目录结构并复制文件名
find 要复制的文件夹 -type d -exec mkdir -p new_dir_copy/{} \;
find 要复制的文件夹 -type f -exec touch new_dir_copy/{} \;

#例子：
find /tmp/大数据文件夹 -type d -exec mkdir -p new_dir_copy/{} \;
find /tmp/大数据文件夹 -type f -exec touch  new_dir_copy/{} \;


