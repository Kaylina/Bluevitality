#### Example
```txt
普通模式：
	v/V			矩形视图模式（逐字符：v，逐行:V。块选择：CTL+v，编辑后按2次ESC退出，注：大'I'进入编辑)
	H、M、L	  		当前屏幕上下移动
	p		  	粘贴："paste"
	dd			删当前行，3dd删除三行
	x / nx			删除光标后面1个字符或n个字符
	i / a			进入编辑模式（在当前行的下行进入编辑模式：o，在当前行前面插入一行：O）
	u    .	  		撤销、重复上次操作（.与ctl+r作用相同）	
	cc			删当前行后进入编辑模式
	^  $			至行首、尾
	d^  d$			从光标到行首、行尾删除
	NG			到第N行，或命令行下：vim +number filename
	gg、G			至档头、档尾
	n<Enter>		向下移动n行，或：ngg
	n<space>		向右移动n个字符
	h、j、k、l		上下左右
	Ctrl + N 、P		在当前文本内向下、上查找以自动补全或提示
	Ctrl + a、x	  	为变量自增、自减（<num> ctl+a  加指定值）
	Ctrl + f、b	  	上下翻页
	w / e			至单词开头或结尾
	yy / y$			复制一行或复制光标所在位置到行末的部分
命令模式：
	1，5s/A/B/g	  	替换1-5行，全局替换：%s/old/new/g
	1，$d			从第1行删到尾行（d$当前删到行尾）
	1，5y			拷贝1-5行	（复制当前行：yy，3yy：复制3行）
	/work ?work	  	向下、向上查找
	s/old/new/g		本行替换	"//"内支持正则表达式
	set nu		    	显示行号（直接输入数字后回车可到达指定行）
	set ic		    	搜索时忽略大小写，即"Ignore Case"的简写
	set ai		    	设置自动缩进（自动对齐）
	set tabstop=4	        按TAB键时的缩进数
	set fileencoding=utf8	指定编码
	set bg=dark		设置背景色
	syntax on     		语法高亮
	r Filename	  	读取并在本行后插入（指定行后插入：nr Filename）
	w Filename		另存为
	n1,n2 w Filename	将n1到n2行之间的数据另存到文件Filename
	split 			创建分屏 (vsplit：创建垂直分屏)
	wq!		   	强制保存并离开
	!command	    	在Vim内的命令模式下执行系统命令
	x             		保存并且退出
	X		        加密保存（需输入密码）

附：
	view Filename		以只读模式查看
	vimdiff	F1 F2	  	在vim视图下比较两文件内容的差异
	
	多文件[o/O]：
		上下分布：	vim  -o 	F1 F2
		左右分布：	vim  -O 	F1 F2
```
