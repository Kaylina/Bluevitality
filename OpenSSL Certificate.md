> 环境：centos 6.5  
OpenSSL Version 1.0.1e  
by inmoonlight@163.com 2017.05.2


## CA环境设置

### 1.设置CA工作目录：/etc/pki/tls/openssl.cnf 
```shell
[ CA_default ]

dir             = /etc/pki/CA           # <-----
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
private_key     = $dir/private/cakey.pem # The private key
RANDFILE        = $dir/private/.rand    # private random number file
```

### 2.初始化CA证书编号初始值
```shell
cd /etc/pki/CA && echo 01 > serial
```
### 3.创建CA根私钥
```shell
CA_dir="/etc/pki/CA"
openssl genrsa -out ${CA_dir:=/etc/pki/CA}/private/cakey.pem 2048
chmod 700 ${CA_dir:=/etc/pki/CA}/private/cakey.pem
```

### 4.创建CA根证书
```shell
CA_dir="/etc/pki/CA"
openssl req -new -x509 -days 3650 -key ${CA_dir:=/etc/pki/CA}/private/cakey.pem \
-out ${CA_dir:=/etc/pki/CA}/cacert.pem

Country Name (2 letter code) [XX]:CN					#国家（大写缩写）
State or Province Name (full name) []:shanghai				#省份或洲
Locality Name (eg, city) [Default City]:shanghai			#城市
Organization Name (eg, company) [Default Company Ltd]:company		#公司
Organizational Unit Name (eg, section) []:yanfa				#部门    
Common Name (eg, your name or your server’s hostname)[]:xx.xx.xx.xx	#须与证书能解析到的名字一致
Email Address []:admin@paybay.cn
#以上参数可通过配置文件修改：/etc/pki/tls/openssl.cnf
```

## Server环境设置
### 1.创建服务器私钥
```shell
mkdir /etc/certs && cd /etc/certs && openssl genrsa -out ./webserv.key 2048
chmod 644 -R /etc/certs/*
```
### 2.服务器证书申请
```shell
openssl req -new -key /etc/certs/webserv.key -out /etc/certs/webserv.csr
Country Name (2 letter code) [AU]:CN                    
State or Province Name (full name) [Some-State]:shanghai
Locality Name (eg, city) []:shanghai
Organization Name (eg, company) [Internet Widgits Pty Ltd]:company
Organizational Unit Name (eg, section) []:yanfa
Common Name (e.g. server FQDN or YOUR name) []:xxx.xxx.xxx.xxx
Email Address []:admin@company.cn
```
### 3.将证书请求:"csr" 传至CA进行签名
```shell
scp /etc/certs/webserv.csr root@<CA_Ip-Address>:/etc/ssl
```
### 4.在CA机构对此csr进行签名
```shell
cd /etc/ssl
openssl x509 -req -in /etc/ssl/webserv.csr -CA /etc/pki/CA/cacert.pem \
-CAkey /etc/pki/CA/private/cakey.pem -CAcreateserial -out webserv.crt
#将签名后的crt传至Server服务器：
scp webserv.crt root@<Server_Ip-Adress>:/etc/certs
```

### 5.在服务端的：ngixn/mqtt/apache中设置使用https
```shell
nginx-example：
ht.. 
	ssl_session_cache   shared:SSL:10..	
	ssl_session_timeout 10m;	.. 
	......
	server {
		listen              443 ssl;
		server_name         example.com
		ssl_certificate     webserv.crt;
		ssl_certificate_key webserv.key;
		ssl_protocols       TLSv1 TLSv1.1 TLSv1.2; 
		ssl_ciphers         HIGH:!aNULL:!MD5;
		add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;	
		add_header X-Content-Type-Options nosniff;    
		add_header X-Xss-Protection 1;		          
		......
	}
}
	
#注：由于是自建CA，客户端或浏览器自身没有此私有CA证书，需在使用前提前导入CA根证书否则S端发来的证书不被C端承认
```

## 在CA端吊销证书

### 1.在S端获取证书serial
```shell
openssl x509 -in /etc/serts/webserv.crt -noout -serial -subject
#stdout-example...
serial=01
subject=/C=CN/ST=shanghai/O=paybay/OU=yanfa/CN=xxx.xxx.xxx.xxx	#保留输出内容供CA端验证
```	
### 2.在CA端验证：	
```shell
cat /etc/pki/CA/index.txt
V	251227084917Z		01	unknown	/C=CN/ST=shanghai/O=paybay/OU=yanfa/CN=xxx.xxx.xxx.xxx
#依S端提交的serial和subject信息来验证与index.txt中的信息是否一致
```

### 3.在CA端吊销：
```shell
openssl ca -revoke newcerts/01.pem
```	 
### 4.CA生成吊销编号（仅在第1次吊销证书时）
```shell
echo 01 > /etc/pki/CA/crlnumber
```
### 5.CA更新证书吊销列表:
```shell
cd /etc/pki/CA/crl &&  openssl ca -gencrl -out ca.crl
```
## 附
### 以命令行方生成X509证书信息（非交互）
```shell
openssl req -new -newkey rsa:2048 -sha256 -nodes -out example.csr -keyout example.key \
-subj "/C=CN/ST=ShenZ/L=ShenZ/O=Example/OU=Web/CN=eg.cn"
```
### 其他常用命令
- 测算法速度：	openssl speed <算法>
- 生成随机数：	openssl rand [ -base64 / -hex ] <length>
- 生成公私钥：	openssl genrsa -out private.key 2048  
				openssl rsa -in private.key -pubout -out public.pubkey
- 文件加解密：	openssl enc -e -des3 -in sec.key -out file.secrite  
				openssl enc -d -des3 -in file.secrite -out sec.key.dec
- 计算摘要值：	openssl [md5/sha1] < file <---> echo -n "***"  
				[ md5sum / sh1sum ] <---> openssl dgst [-md5/sha1] < file

