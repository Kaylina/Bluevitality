#### 参数
```txt
-g gateway source-routing hop point[s], up to 8
-G num source-routing pointer: 4, 8, 12, …
-i secs 延时的间隔
-w secs timeout的时间
-l 监听模式，用于入站连接
-p port 本地端口号
-u UDP模式
-s addr 本地源地址
-n 指定数字的IP地址，不能用hostname
-z 将输入输出关掉——用于扫描时，其中端口号可以指定一个或者用lo-hi式的指定范围。
-o file 记录16进制的传输
-r 任意指定本地及远程端口
-v 详细输出(可用多个）
```


#### Example
```bash
nc -u -l -p 3306    #以UDP模式监听本地3306端口

nc -s 192.168.1.2 192.168.1.1 3306  #使用本地的192.168.1.2连接远程的192.168.1.1:3306

#从192.168.2.33拷贝文件到192.168.2.34
nc -l 1234 > test.txt       #在192.168.2.34上
nc 192.168.2.34 < test.txt  #在192.168.2.33上
#或者：
cat a.txt | nc 192.168.0.3  9999        #发送端
nc -l 9999 > a.txt                      #接收端

#端口扫描
nc -v -w 2 192.168.2.34 -z 21-24
# nc: connect to 192.168.2.34 port 21 (tcp) failed: Connection refused
# Connection to 192.168.2.34 22 port [tcp/ssh] succeeded!
# nc: connect to 192.168.2.34 port 23 (tcp) failed: Connection refused
# nc: connect to 192.168.2.34 port 24 (tcp) failed: Connection refused

#用nc命令操作memcached
printf “set key 0 10 6\r\nresult\r\n” |nc 192.168.2.34 11211  	#存储数据
printf “get key\r\n” |nc 192.168.2.34 11211                   	#获取数据
printf “delete key\r\n” |nc 192.168.2.34 11211                	#删除数据
printf “stats\r\n” |nc 192.168.2.34 11211                     	#查看状态
watch “echo stats” |nc 192.168.2.34 11211      #模拟top命令查看状态
printf “flush_all\r\n” |nc 192.168.2.34 11211 					#清空缓存
```
