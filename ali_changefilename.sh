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
for A in 1400{1..4};
{	    #第二层目录
            for B in {digital,poems,phrase};
            {
		     #进入目录后将以SI开头的文件交给awk。以关键字:"_number_"做分隔，变量"li"是当前所在目录名 输出:"mv 原名 新名" 并交给Bash
                     cd ${A}/${B} && ls SI* | awk -F "_number_" -v P="$(basename $(pwd))" '{print "mv " $0 " " $1 "_" P "_" $2}' | bash -
		     #执行完后返回脚本所在目录（在"数据大文件夹"这个目录下执行）
                     cd ../..
            }
}

#--------------------------------------------------------------------------
#复制目录结构并复制文件名
find /tmp/大数据文件夹 -type d -exec mkdir -p new_dir_copy/{} \;
find /tmp/大数据文件夹 -type f -exec touch  new_dir_copy/{} \;

#恢复错误：（可执行多次）
find . -type f | grep -v "wav$" | awk -F".wav" '{print "mv "$0 " "$1".wav" }' | bash -

#-------------------------------------------------------------------------- 更直接的：
#找出当前目录开始其内部所有以SI开头并且以wav结尾的文件，输出格式："mv 旧文件名 新文件名" 然后交给bash去执行这个命令（可以重复执行，没影响）
find . -type f -name "SI_*wav"  | grep number | awk -F"_number_|/"  '{print $0"-->"$(NF-2)}' | awk -F'-->|_number_' '{print "mv "$1"_number_"$2" "$1"_"$3"_"$2}' | bash -

