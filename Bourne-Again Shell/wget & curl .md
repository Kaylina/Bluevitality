#### wget
```txt
wget  -cbQ 1M t 0 p ~/downloads -i ~/downloadFiles

-c	断点续传 connection
-b	后台下载 backend
-Q	限速，或：-–limit-rate=300k
-p	保存路径
-t	重试次数，或：--tries=0，不停重试：-t 0	
-T	设置超时时间
-i	从指定文件下载多个，或：--input-file=/path/filename
-m	镜像，或： --mirror，等价于： -r -N -l inf -nr
-d	输出DEBUG信息
-v	详细输出模式（默认）
-q	不输出任何信息

认证：
	HTTP：	
		--http-user=*****
		--http-password=*****			
	FTP：		
		--user=<NAME> 	
		--password=<PASS>
		--passive-ftp		被动传输 (缺省) 
		--active-ftp		主动传输
        
代理：
	-U, --user-agent=AGENT	指定客户端为指定设备（默认情况下Agent为wget）
	--no-http-keep-alive 	不使用HTTP keep-alive
	--no-cookies 		不使用 cookie
	--no-check-certificate	不检查证书
	--header "name: value"	自定义HTTP头
	--load-cookies=档案     使用指定 cookie
	--save-cookies=档案     将cookie存至指定位置
	--keep-session-cookies 	载入和储存暂时性的cookie
	代理服务器：	
    若需经过代理服务器，可让wget通过代理服务器进行下载。此时需在当前家目录创建.wgetrc并中设置代理服务器：
		--proxy=on/off 
		http-proxy = ip:port
		ftp-proxy = ip:port
		若代理服务器需要密码则使用： 
		 	--proxy-user=
		 	--proxy-passwd=
整站下载：
	wget -r -N -l 3 -k URL
	-l	指定下载的页面层级（与-r一同使用）
	-r  递归下载站上所有目录和文件，其指向的链接同样被下载
	-N  使用文件的时间戳
	-k  将页面链接转换为本地地址
	文件类型：
		--reject=gif		忽略的文件类型
		--accept=jpeg		接受的文件类型
```

#### curl
```txt
# curl可构造http请求。是利用URL规则在命令行下工作的文件传输工具。支持文件上传/下载，是综合传输工具

curl参数：
	-c <file> 	保存服务器的cookie文件
	-E cert.pem 指定本地证书
	-I  		自定义header信息（HTTP头）
	-x		设置代理	curl -x proxysever.com:3128 http://google.com
	-L 		当页面有跳转时输出跳转到的页面
	-T		上传到服务器	curl -u ftpu:ftp -T Filename ftp://testserver.com
	-u 		使用用户名和密码登陆 curl -u ftpu:ftp -O ftp://server/public/x.php（或仅输入账号）
	-A/--user-agent <string> 设置用户代理发送给服务器
　	-e/--referer 		来源网址
	-H/--header <line>	 自定义头信息传递给服务器
	--cookie <name=string/file>  cookie字符串或文件读取位置
	--connect-timeout <s> 	设置超时时间
	--limit-rate <rate> 	限速 curl --limit-rate 10000B www.baidu.com
	--negotiate     	使用HTTP身份验证
	--local-port		强制使用指定的本地端口
	--digest        	使用数字身份验证
	--key <key>    		私钥文件名 (SSL)
	--key-type <type> 	私钥文件类型 (DER/PEM/ENG) (SSL)
	--pass  <pass>  	私钥密码 (SSL)
	--cacert <file> 	CA证书 (SSL)
	--capath <directory> 	CA目录


root@paybay:~# curl -I www.baidu.com		脚本查看http头信息： curl -I -s <url>
HTTP/1.1 200 OK
Date: Tue, 05 Jan 2016 02:11:36 GMT
Content-Type: text/html; charset=utf-8
Connection: Keep-Alive
Vary: Accept-Encoding
Set-Cookie: PSTM=1451959896; expires=Thu, 31-Dec-37 23:55:55 GMT; max-age=2147483647; path=/; domain=.baidu.com
Set-Cookie: BDSVRTM=0; path=/
Set-Cookie: BD_HOME=0; path=/
P3P: CP=" OTI DSP COR IVA OUR IND COM "
Cache-Control: private
Expires: Tue, 05 Jan 2016 02:10:55 GMT
X-Powered-By: HPHP
Server: BWS/1.1
X-UA-Compatible: IE=Edge,chrome=1
BDPAGETYPE: 1

实现post/get请求：
	post：	curl -u username --data "param1=value1&param2=value" https://api.github.com	
	get：	curl -u username https://api.github.com/user?access_token=XXXXXXXXXX
```

#### Example
```bash
[root@localhost ~]# curl www.baidu.com -v > /dev/null  -s
* About to connect() to www.baidu.com port 80 (#0)
*   Trying 220.181.112.244...
* Connected to www.baidu.com (220.181.112.244) port 80 (#0)
> GET / HTTP/1.1
> User-Agent: curl/7.29.0
> Host: www.baidu.com
> Accept: */*
> 
< HTTP/1.1 200 OK
< Server: bfe/1.0.8.18
< Date: Tue, 31 Oct 2017 06:18:16 GMT
< Content-Type: text/html
< Content-Length: 2381
< Last-Modified: Mon, 23 Jan 2017 13:27:36 GMT
< Connection: Keep-Alive
< ETag: "588604c8-94d"
< Cache-Control: private, no-cache, no-store, proxy-revalidate, no-transform
< Pragma: no-cache
< Set-Cookie: BDORZ=27315; max-age=86400; domain=.baidu.com; path=/
< Accept-Ranges: bytes
< 
{ [data not shown]
* Connection #0 to host www.baidu.com left intact
```
