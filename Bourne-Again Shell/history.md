####　Example
```bash
# Linux系统当你在shell(控制台)中输入并执行命令时，shell会自动把你的命令记录到历史列表中
# 一般保存在用户目录下的.bash_history文件中。默认保存1000条，你也可以更改这个值。

[root@localhost ~]# history -c  #清空当前SHELL的所有历史记录
[root@localhost ~]# history -a  #将目前的history指令写入histfiles中，若没指定histfiles则写入：~/.bash_history
[root@localhost ~]# history -w  #将目前的history指令写入histfiles中
[root@localhost ~]# history -r  #将 histfiles 的内容读到目前这个 shell 的 history 记忆中

[root@localhost ~]# history 20  #

[root@localhost ~]# !23         #指定历史记录中的第23条命令
[root@localhost ~]# !command:p  #只显示而不执行特定关键字开头的命令
[root@localhost ~]# !!          #执行上一条命令
[root@localhost ~]# !cmd        #执行以cmd关键字开头的最近一条命令
```
