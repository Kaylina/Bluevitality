> VNC Install & configure

## 安装
```Bash
#yum install -y libdevmapper*   #若Gnome安装失败则执行此命令
#yum install -y docker          #若Gnome安装失败则执行此命令

#安装 Gnome 包
yum -y groupinstall "GNOME Desktop" "Graphical Administration Tools"

#修改系统运行级别
ln -sf /lib/systemd/system/runlevel5.target/etc/systemd/system/default.target

yum check-update
yum install tigervnc-server -y
```

## 配置
修改配置信息：cp /lib/systemd/system/vncserver@.service /etc/systemd/system/vncserver@:`1`.service
#### 
```Bash
vim /etc/systemd/system/vncserver@:1.service
#打开文件后找到这一行
ExecStart=/sbin/runuser -l <USER> -c "/usr/bin/vncserver %i"
PIDFile=/home/<USER>/.vnc/%H%i.pid

#这里直接用root登录，所以替换成
ExecStart=/sbin/runuser -l root -c "/usr/bin/vncserver %i"
PIDFile=/root/.vnc/%H%i.pid

#如果是其他用户的话，如john
ExecStart=/sbin/runuser -l <USER> -c "/usr/bin/vncserver %i"
PIDFile=/home/<USER>/.vnc/%H%i.pid
```
```Bash
#重启服务
systemctl daemon-reload
#为VNC设密码
vncpasswd
```
#### 防火墙设置
```Bash
-A INPUT -m state --state NEW -m tcp -p tcp --dport 5900:5903 -j ACCEPT
service iptables restart
#或：
firewall-cmd --permanent --add-service vnc-server #可能出错，忽略
systemctl restart firewalld.service
```
#### 自启
```Bash
systemctl enable vncserver@:1.service
systemctl restart firewalld.service
```

#### 说明
VNC服务本身使用的是5900端口。鉴于有不同的用户使用 VNC ，每个人的连接都会获得不同的端口。  
配置文件名里面的数字告诉 VNC 服务器把服务运行在5900的子端口上。  
在这个例子里，第一个服务会运行在5901（5900+1）端口上，之后依次增加，运行在5900 + x 端口上。  
其中 x 是指之后用户的配置文件名 vncserver@:x.service 里面的 x 
