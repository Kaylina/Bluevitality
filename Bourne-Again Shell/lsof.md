#### Example
```bash
lsof abc.txt          #显示开启文件abc.txt的进程
lsof -c abc           #显示abc进程现在打开的文件
lsof -c -p 1234       #列出进程号为1234的进程所打开的文件
lsof -g gid           #显示归属gid的进程情况
lsof +d /usr/local/         #显示目录下被进程开启的文件
lsof +D /usr/local/         #同上，但是会搜索目录下的目录，时间较长
lsof -u1000                   #查看uid是100的用户的进程的文件使用情况
lsof -c courier -u ^zahn      #显示出那些文件被以courier打头的进程打开，但是并不属于用户zahn
lsof -i           #显示所有打开的端口
lsof -i:80        #显示所有打开80端口的进程
```
