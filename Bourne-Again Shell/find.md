### 参数汇总
```bash
-name       按文件名查找： find -name "*.txt" cp -ap {} {}.bkup \;
-iname      按文件名查找：find -iname "MyCProgram.c"（不匹配大小写，相当于grep -rl "MyCProgram.c" .）
-maxdepth   最大目录搜索深度：find / -maxdepth 10 -exec basename {} \; (仅输出指定目录深度下的文件名 )
-mindepth   最小目录搜索深度：find / -maxdepth 5 -mindepth 2 -name "*.conf" -exec ls -l {} \;
-exec       对搜索结果执行的操作：find -name "*.html" -exec ./bash_script.sh '{}' \;
-not        相反匹配：find -maxdepth 1 -not -iname "被排除的文件名"
-inum       使用文件系统inode号查找文件：find -inum 804180 -exec rm {} \;
-perm       按对象权限类型搜索（格式：-perm -u=rwx / -perm 0777 ）
-type       搜索文件类型（f,d,s,c,b,...）：find . -type f -iname “*.mp3″ -exec rename “s/ /_/g” {} \;
-empty      内容为空的文件：find / -empty （注：当搜索路径被指定为绝对路径时其输出也是绝对路径！）
-size       指定小于或大于特定大小的文件：find / -size +60k -exec ls -hl {} \;
-mmin       指定小于或大于分钟范围内容被修改过的文件
-mtime      指定小于或大于天数范围内容被修改过的文件：find -iname "*.conf" -exec md5sum {} \;
-amin       指定小于或大于分钟范围被访问过的：find -mmin -/+60 -exec ls -l {} \;
-atime      指定小于或大于天数范围被访问过的：find -atime -/+1
-cmin       指定小于或大于分钟范围被修改过内容的
-ctime      指定小于或大于天数范围被修改过内容的
-never      查找比某一文件修改时间还要新的文件：find -newer /etc/passwd
-anewer     查找比某一文件访问时间还要新的文件
-cnever     查找比某一文件状态改变时间还要新的文件
-xdev       仅在当前文件系统中搜索： find / -xdev -name "*.log"
-user       指定用户的文件：find / -user root
-nouser     无属主的
-nogroup    无属组的
-readable   可读的
-writable   可写的
-fstype     属于特定文件类型的
-gid        特定属组ID的文件
-delete     对搜索结果直接执行删除动作
```
### find --help
```bash
Usage: find [-H] [-L] [-P] [-Olevel] [-D help|tree|search|stat|rates|opt|exec] [path...] [expression]

default path is the current directory; default expression is -print
expression may consist of: operators, options, tests, and actions:

operators (decreasing precedence; -and is implicit where no others are given):
      ( EXPR )   ! EXPR   -not EXPR   EXPR1 -a EXPR2   EXPR1 -and EXPR2
      EXPR1 -o EXPR2   EXPR1 -or EXPR2   EXPR1 , EXPR2

positional options (always true): -daystart -follow -regextype

normal options (always true, specified before other expressions):
      -depth --help -maxdepth LEVELS -mindepth LEVELS -mount -noleaf
      --version -xdev -ignore_readdir_race -noignore_readdir_race

tests (N can be +N or -N or N): -amin N -anewer FILE -atime N -cmin N
      -cnewer FILE -ctime N -empty -false -fstype TYPE -gid N -group NAME
      -ilname PATTERN -iname PATTERN -inum N -iwholename PATTERN -iregex PATTERN
      -links N -lname PATTERN -mmin N -mtime N -name PATTERN -newer FILE
      -nouser -nogroup -path PATTERN -perm [+-]MODE -regex PATTERN
      -readable -writable -executable
      -wholename PATTERN -size N[bcwkMG] -true -type [bcdpflsD] -uid N
      -used N -user NAME -xtype [bcdpfls]

actions: -delete -print0 -printf FORMAT -fprintf FILE FORMAT -print
      -fprint0 FILE -fprint FILE -ls -fls FILE -prune -quit
      -exec COMMAND ; -exec COMMAND {} + -ok COMMAND ;
      -execdir COMMAND ; -execdir COMMAND {} + -okdir COMMAND ;
```
参考：  
http://www.oschina.net/translate/15-practical-unix-linux-find-command-examples-part-2
http://www.oschina.net/translate/15-practical-linux-find-command-examples
