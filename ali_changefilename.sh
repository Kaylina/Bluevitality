#创建环境：
mkdir 1400{1..4}/{digital,poems,phrase} -p
touch 1400{1..4}/digital/SI_devide4_number_{01..15}.wav
touch 1400{1..4}/poems/SI_devide4_number_{16..30}.wav
touch 1400{1..4}/phrase/SI_devide4_number_{31..60}.wav

#--------------------------------------------------------------------------
	
开始修改：
#!/bin/bash
#这个要在数据大文件夹下面执行，比如/数据大文件夹/1400.... 就创建在：数据大文件夹/shell.sh ，然后执行：bash shell.sh

#第一层目录
for n1 in 1400{1..4};
{			#第二层目录
            for n2 in {digital,poems,phrase};
            {
					 #进入目录... 列出SI开头的文件... 以关键字:"_number_"做分隔符... 变量"li"是当前所在的的目录名 输出:"mv 原文件名 新文件名" 并交给Bash去执行这个字串
                     cd ${n1}/${n2} &&  ls SI* | awk -F "_number_" -v li="$(basename $(pwd))" '{print "mv " $0 " "  $1 "_" li "_" $2}' | bash -
					 #执行完之后返回执行这个脚本的所在目录，不然下一次的循环执行路径不对会有问题（脚本要在"数据大文件夹"这个目录下执行）
                     cd ../..
            }
}




#复制目录结构并复制文件名（不会复制文件内容，所以不占空间）：这样就会把整个目录结构拷贝一份到新的new_dir_copy文件夹下
find 要复制的文件夹 -type d -exec mkdir -p new_dir_copy/{} \;
find 要复制的文件夹 -type f -exec touch new_dir_copy/{} \;

#例子：
find /tmp/大数据文件夹 -type d -exec mkdir -p new_dir_copy/{} \;
find /tmp/大数据文件夹 -type f -exec touch  new_dir_copy/{} \;


