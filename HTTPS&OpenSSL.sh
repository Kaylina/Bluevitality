#openssl自建CA & https
#环境：centos 6.5 - OpenSSL Version 1.0.1e
#by inmoonlight@163.com 2017.05.2

vim /etc/pki/tls/openssl.cnf 
#查看OpenSSL中CA的工作目录，在41行~56行，翻译：http://www.178linux.com/10705
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

cd /etc/pki/CA && echo 01 > serial		#设置证书编号初始值


在PKI的CA端：

	创建CA根私钥：
		#设置CA工作目录
		CA_dir="/etc/pki/CA"
		#创建CA根的私钥并设置私钥权限
		openssl genrsa -out ${CA_dir:=/etc/pki/CA}/private/cakey.pem 2048 && chmod 700 ${CA_dir:=/etc/pki/CA}/private/cakey.pem
		
	创建CA根证书：
		CA_dir="/etc/pki/CA"
		#创建CA的根证书
		openssl req -new -x509 -days 3650 -key ${CA_dir:=/etc/pki/CA}/private/cakey.pem -out ${CA_dir:=/etc/pki/CA}/cacert.pem 
		Country Name (2 letter code) [XX]:CN            		#国家（大写缩写）
		State or Province Name (full name) []:shanghai  		#省份或洲
		Locality Name (eg, city) [Default City]:shanghai		#城市
		Organization Name (eg, company) [Default Company Ltd]:paybay   #公司
		Organizational Unit Name (eg, section) []:yanfa  		#部门    
		Common Name (eg, your name or your server’s hostname) []:xxx.xxx.xxx.xxx #地址须与证书所有者能解析到的名字一致！（IP or domain）
		Email Address []:admin@paybay.cn
		#以上参数可通过配置文件修改：/etc/pki/tls/openssl.cnf

在PKI的Server端：

	创建服务器私钥：
		mkdir /etc/certs && cd /etc/certs && openssl genrsa -out ./webserv.key 2048
		chmod 644 -R /etc/certs/*
		
	服务器证书申请：
		openssl req -new -key /etc/certs/webserv.key -out /etc/certs/webserv.csr
		Country Name (2 letter code) [AU]:CN                    
		State or Province Name (full name) [Some-State]:shanghai
		Locality Name (eg, city) []:shanghai
		Organization Name (eg, company) [Internet Widgits Pty Ltd]:paybay
		Organizational Unit Name (eg, section) []:yanfa
		Common Name (e.g. server FQDN or YOUR name) []:xxx.xxx.xxx.xxx
		Email Address []:admin@paybay.cn
		
	将证书请求:"csr" 传至CA进行签名：
		scp /etc/certs/webserv.csr root@<CA_Ip-Address>:/etc/ssl
		
	在CA机构对此csr进行签名：
		cd /etc/ssl
		openssl x509 -req -in /etc/ssl/webserv.csr -CA /etc/pki/CA/cacert.pem -CAkey /etc/pki/CA/private/cakey.pem -CAcreateserial -out webserv.crt
		#将签名后的crt传至Server服务器：
		scp webserv.crt root@<Server_Ip-Adress>:/etc/certs
			
		
	在服务端的：ngixn/mqtt/apache中设置使用https
	nginx-example：
	
	http {
		ssl_session_cache   shared:SSL:10m;		#配置共享会话缓存大小
		ssl_session_timeout 10m;				#设置HTTPS的会话超时时间
		#...
			server {
				listen              443 ssl;	#ssl参数
				server_name         example.com
				ssl_certificate     webserv.crt;			#证书
				ssl_certificate_key webserv.key;			#私钥（私钥作为安全实体，应被放在有一定权限限制的目录并保证Nginx主进程有存取权)
				ssl_protocols       TLSv1 TLSv1.1 TLSv1.2;	#ssl_protocols 和 ssl_ciphers 限制连接含 SSL/TLS 的加強版本&算法
				ssl_ciphers         HIGH:!aNULL:!MD5;
				add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;	#HSTS策略	
				add_header X-Content-Type-Options nosniff;	#禁止服务器自动解析资源类型
				add_header X-Xss-Protection 1;				#防XSS攻击
				#...
			}
	}


#注意：由于是自建CA，客户端或浏览器自身没有此私有CA证书，需在使用前提前导入CA根证书否则S端发来的证书不被C端承认


在CA端吊销证书：

	在S端获取证书serial：
		openssl x509 -in /etc/serts/webserv.crt -noout -serial -subject
		#stdout-example...
		serial=01
		subject=/C=CN/ST=shanghai/O=paybay/OU=yanfa/CN=xxx.xxx.xxx.xxx	#保留输出内容供CA端验证
		
	在CA端验证：	#依S端提交的serial和subject信息来验证与index.txt中的信息是否一致
		cat /etc/pki/CA/index.txt
		V	251227084917Z		01	unknown	/C=CN/ST=shanghai/O=paybay/OU=yanfa/CN=xxx.xxx.xxx.xxx
		
	在CA端吊销：
		 openssl ca -revoke newcerts/01.pem
		 
	CA生成吊销编号（仅在第一次吊销证书时）：
		echo 01 > /etc/pki/CA/crlnumber
	
	CA更新证书吊销列表:
		cd /etc/pki/CA/crl &&  openssl ca -gencrl -out ca.crl
	
	




#附例子：（脚本实现时使用，以命令行方式填写x509证书信息）
openssl req -new -newkey rsa:2048 -sha256 -nodes -out example.csr -keyout example.key -subj "/C=CN/ST=ShenZ/L=ShenZ/O=Example/OU=Web/CN=eg.cn"







