# Stunnel

Stunnel可加密网络数据的TCP连接
采用C/S将CIient端数据采用SSL加密，安全传输到指定的Server端再解密还原然后发送到目的端口
其使用TLS对tcp协议进行加密

## 安装
```BASH
    wget http://www.stunnel.org/download/stunnel/src/stunnel-4.33.tar.gz
    tar zxvf stunel-4.33.tar.gz
    ./configure;make ; make install
```
## 创建CA根私钥及根证书
```BASH
    openssl genrsa -des3 -out /etc/pki/CA/rootca.key 1024
    openssl req -new -x509 -key /etc/pki/CA/rootca.key -out /etc/pki/CA/rootca.crt -days 365
```
##  用CA根证书对子证书授权：
```BASH
    openssl genrsa -des3 -out ~/Mysql-master.key 1024  #用户自身的私钥
    openssl req -new -key ~/Mysql-master.key -out ~/Mysql-master.csr  #用户自身的证书
    scp Susers.csr root@CA-IP:/ca/  #拷贝到CA进行签名
    #在CA端对csr请求签名：
        touch /etc/pki/CA/{index.txt,serial}
        echo "01" > /etc/pki/CA/serial
        openssl ca -keyfile /etc/pki/CA/rootca.key -cert /etc/pki/CA/rootca.crt -in ./Mysql-master.csr -out ./Mysql-master.pem -days 365
```

### 隧道环境：  
[Master@192.168.1.2:3306 -- stunnel:3508] ------  [stunnel:3408 -- Slave@192.168.1.1]


### 配置说明：/etc/stunnel/stunnel.conf
**Server 端：**
```BASH
    client=no #服务端
    compression=zlib 
    syslog=yes 
    debug=7 
    output=/var/log/stunnel.log 
    setuid=root 
    setgid=root 
    pid=/var/run/stunnel.pid         
    cert=/etc/ssl/cert/Mysql-master.pem #证书
    key=/etc/ssl/private/Mysql-master.key #私钥
    #CAfile = /etc/pki/CA/certs/rootca.crt #根证书
    [mysql] 
    accept=3306 #监听本地的3508连接请求并对其数据加密
    connect=192.168.1.2:99999  #监听本机192.168.1.2:3306端口的加密数据
```
    
**Client 端：**
```BASH
    client=yes 
    pid=/tmp/stunnel.pid 
    debug=7 
    foreground=no 
    verify=0  #认证?（如需认证则双方都使用SSL）
    #CAfile = /etc/pki/CA/certs/rootca.crt  根证书
    [mysql] 
    accept=99999 #监听本地的3408连接请求并对其数据加密
    connect=192.168.1.2:3306 #即将本机监听到的3508加密数据转交给3408解密（mysql客户端连接到3408即可）
$$E=mc^2$$
```


参考：
http://www.cnblogs.com/bluevitality/p/6652688.html

https://blog.lilydjwg.me/2012/10/25/secure-your-http-proxy-with-tls-ssl.36107.html    
