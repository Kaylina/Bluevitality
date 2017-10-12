 nu              "显示行号
 2 set numberwidth=2   "行号宽度
 3 set encoding=utf-8  "编码
 4 set cursorline      "突出显示当前行
 5 set tabstop=4       "制表符4个空格
 6 set incsearch       "输入搜索内容时就显示搜索结果
 7 
 8 
 9 map l dd            "使用l替代dd
10 map <space> 2j      "使用空格替代跳转到下2行
11 map <c-d>   dd      "Ctrl+d ---> dd
12 nnoremap jyh o<esc>k "当前行后再插入一行
13 nnoremap fgx i#---------------------------------------------------<esc>j    "分割线                                                                          
14 nnoremap 2gp <esc>:vsplit<cr>   #竖屏分割
15 
