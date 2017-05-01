#!/bin/bash
#使用openssl自建CA - 设置Nginx的https
#环境：centos 6.5 - OpenSSL Version 1.0.1e
#by inmoonlight@163.com 2017.04.29

vim /etc/pki/tls/openssl.cnf #了解CA环境

#在41行~56行（查找CA的工作目录）翻译：http://www.178linux.com/10705
[ CA_default ]

dir             = /etc/pki/CA           # Where everything is kept
certs           = $dir/certs            # Where the issued certs are kept
crl_dir         = $dir/crl              # Where the issued crl are kept
database        = $dir/index.txt        # database index file.
#unique_subject = no                    # Set to 'no' to allow creation of
                                        # several ctificates with same subject.
new_certs_dir   = $dir/newcerts         # default place for new certs.

certificate     = $dir/cacert.pem       # The CA certificate
serial          = $dir/serial           # The current serial number
crlnumber       = $dir/crlnumber        # the current crl number
                                        # must be commented out to leave a V1 CRL
crl             = $dir/crl.pem          # The current CRL
private_key     = $dir/private/cakey.pem# The private key
RANDFILE        = $dir/private/.rand    # private random number file


#确保/etc/pki/CA目录下有private，newcerts，crl目录及index.txt，serial文件
#private：	存放CA自身私钥

cd /etc/pki/CA && echo 01 > serial		#设置证书编号初始值


服务端：（CA证书设施）
	创建CA根的私钥：（不能外泄！）
		#设置CA的工作目录
		CA_dir="/etc/pki/CA"
		#创建CA根的私钥
		openssl genrsa -out ${CA_dir:=/etc/pki/CA}/private/cakey.pem 2048
		#设置私钥权限
		chmod 700 ${CA_dir:=/etc/pki/CA}/private/cakey.pem
		
	创建CA的根证书：
		#设置CA的工作目录
		CA_dir="/etc/pki/CA"
		#创建CA的根证书
		openssl req -new -x509 -days 3650 -key ${CA_dir:=/etc/pki/CA}/private/cakey.pem -out ${CA_dir:=/etc/pki/CA}/cacert.pem 
		Country Name (2 letter code) [XX]:CN            #国家（大写缩写）
		State or Province Name (full name) []:shanghai  #省份或洲
		Locality Name (eg, city) [Default City]:shanghai#城市
		Organization Name (eg, company) [Default Company Ltd]:paybay   #公司
		Organizational Unit Name (eg, section) []:yanfa  #部门    
		Common Name (eg, your name or your server's hostname) []:xxx.xxx.xxx.xxx #主机（必须与证书所有者能解析到的名字保持一致（即服务器的IP或域名）否则将无法通过验证
		Email Address []:admin@paybay.cn
		#以上操作默认选项可通过修改配置文件（/etc/pki/tls/openssl.cnf）修改

客户端：（web服务端）
	为服务器生成ssl密钥，首先创建ssl目录：
		mkdir /etc/certs && cd /etc/certs
		#创建web服务端的私钥
		openssl genrsa -out /etc/certs/webserv.key 2048
		
		#创建web服务端的证书签名申请文件
		openssl req -new -key /etc/certs/webserv.key -out /etc/certs/webserv.csr
		Country Name (2 letter code) [AU]:CN                    
		State or Province Name (full name) [Some-State]:shanghai
		Locality Name (eg, city) []:shanghai
		Organization Name (eg, company) [Internet Widgits Pty Ltd]:paybay
		Organizational Unit Name (eg, section) []:yanfa
		Common Name (e.g. server FQDN or YOUR name) []:xxx.xxx.xxx.xxx #主机（必须与证书所有者能解析到的名字保持一致（即服务器的IP或域名）否则将无法通过验证
		Email Address []:admin@paybay.cn
		
	将证书请求csr传至CA服务器进行签名：
		scp /etc/certs/webserv.csr root@<CA机构的ip地址>:/etc/ssl
		
	在CA机构对此csr进行签名：
		openssl x509 -req -in /etc/ssl/webserv.csr -CA /etc/pki/CA/cacert.pem -CAkey /etc/pki/CA/private/cakey.pem -CAcreateserial -out webserv.crt
		#将生成的webserv.crt传至web服务器中
		scp webserv.crt root@<webserver的ip地址>:/etc/certs
		
		
		
	在web服务端的（ngixn/mqtt/apache）中，设置使用https的方式，并设置证书（crt）以及私钥（key）所在路径
	nginx例：
	
	http {
		ssl_session_cache   shared:SSL:10m;	#配置共享会话缓存大小
		ssl_session_timeout 10m;			#设置HTTPS的会话超时时间
		#...
			server {
				listen              443 ssl;	#ssl参数
				server_name         example.com
				ssl_certificate     webserv.crt;			#证书文件
				ssl_certificate_key webserv.key;			#私钥文件(私钥作为安全实体，应被放在有一定权限限制的目录并保证Nginx主进程有存取权限。)
				ssl_protocols       TLSv1 TLSv1.1 TLSv1.2;	#ssl_protocols 和 ssl_ciphers 用来限制连接只包含 SSL/TLS 的加強版本和算法
				ssl_ciphers         HIGH:!aNULL:!MD5;
				add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;	#HSTS策略	
				add_header X-Content-Type-Options nosniff;	##禁止服务器自动解析资源类型
				add_header X-Xss-Protection 1;	#防止XSS攻击
				#...
			}
	}
		
		
	
记,重启web服务


注意：
	由于是自建的CA，所以客户端或浏览器自身没有CA的证书，需要在使用前提前导入CA根证书，否则S端发来的证书不会被C端承认


吊销证书：
	在客户端，获取证书的serial：
		openssl x509 -in /etc/serts/webserv.crt -noout -serial -subject
		输出例子：（保留输出内容，供CA端进行验证）
		serial=01
		subject=/C=CN/ST=shanghai/O=paybay/OU=yanfa/CN=xxx.xxx.xxx.xxx
	在CA端验证：（根据节点提交的serial和subject信息来验证与index.txt文件中的信息是否一致）
		cat /etc/pki/CA/index.txt
		V	251227084917Z		01	unknown	/C=CN/ST=shanghai/O=paybay/OU=yanfa/CN=xxx.xxx.xxx.xxx
	在CA端吊销证书：
		 openssl ca -revoke newcerts/01.pem
	CA生成吊销证书编号(在第一次吊销时)
		echo 01 > /etc/pki/CA/crlnumber
	CA更新证书吊销列表:
		cd /etc/pki/CA/crl
		openssl ca -gencrl -out ca.crl
	
	




附加网络例子：（脚本实现时用到，命令行方式填写x509信息）
openssl req -new -newkey rsa:2048 -sha256 -nodes -out example_com.csr -keyout example_com.key -subj "/C=CN/ST=ShenZhen/L=ShenZhen/O=Example Inc./OU=Web Security/CN=example.com"







