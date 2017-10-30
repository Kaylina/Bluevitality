# deploy NTP server for Linux
# file: deploy_ntp_server.shell

# 运行本脚本的前提：
# 1. 配置好了YUM服务

# 变量
sys_file_ntp_conf="/etc/ntp.conf"
cust_backup_dir="/tmp"

ntp_server_ip="192.168.232.130"
ip_network=`echo "$ntp_server_ip" | awk -F. '{print $1"."$2"."$3".0"}'`

# 每次等待间隔（单位：秒）
sleep_sec="60"

# 运行时

# 脚本开始
echo "%%%%%%%%%%% start: `date`"

# 系统配置
echo "@@@ Linux: stop/disable iptables."
service iptables stop
chkconfig iptables off

echo "@@@ Linux: disable SELinux"
#setenforce 0

# 安装
echo "@@@ YUM: install ntp*.rpm"
echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
yum install -y ntp
echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
echo ""

# 设置开机启动服务
echo "---- ntpd: chkconfig on"
chkconfig ntpd on
echo ""

# 配置
echo "@@@ NTP - config: backup origin conf file"
echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
cp -rf $sys_file_ntp_conf $cust_backup_dir
echo ""

echo "@@@ NTP - config: edit before everything"
sed -i "/server/s/^server/#server/g" $sys_file_ntp_conf
sed -i "/::1/s/^restrict/#restrict/g" $sys_file_ntp_conf

# 修改NTP的配置文件：ntp.conf
cat <<NTP >> $sys_file_ntp_conf

# Adamhuan Edit
# 需要新增的内容

# Restrict - 关闭所有NTP联机服务
#restrict default ignore

# Restrict - Allow:  IP（需要哪个IP访问NTP服务，可以本机，也可以是其他的主机）
#restrict 127.0.0.1
restrict $ntp_server_ip

# Restrict - Allow: Network（需要哪个网段的IP访问NTP服务）
# 默认添加当前服务器IP所在的网段
restrict $ip_network mask 255.255.255.0 nomodify nopeer kod
# 额外添加的网段
#eg:
#restrict 192.168.130.0 mask 255.255.255.0 nomodify

# Restrict - Deny - Network（不允许哪个网段的访问NTP服务）
#eg:
#restrict 192.168.2.0 mask 255.255.255.0 notrust

# 允许任何IP的客户端访问时间服务
#restrict default nomodify notrap

# 拒绝任何IP的客户端访问时间服务（除了明文允许的）
# 方式一：
#restrict default nomodify notrap noquery
#restrict default notrust
# 方式二：
#restrict 0.0.0.0 mask 0.0.0.0 notrust

# NTP - 服务器优先级（prefer最优先，其他的随意）
# 默认当前时间服务器最优先
server	127.127.1.0	# local clock
server $ntp_server_ip prefer

# 额外的时间服务器
#eg:
#server time-nw.nist.gov
#server s1b.time.edu.cn	

# 结束

NTP

echo "@@@ file - $sys_file_ntp_conf:"
echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
ls -ltr --time-style="+%Y-%m-%d %H:%M |" $sys_file_ntp_conf
echo "*************"
cat $sys_file_ntp_conf
echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
echo ""

# 启用
service ntpd restart

# 查看状态
echo "@@@ NTP - status:"
echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
echo "---- ntp - version:"
ntpq -c version
echo ""

echo "---- sleep $sleep_sec, for ntp re-start done."
while_count=1

while [ `ntpstat | grep "time correct to within" | wc -l` == 0 ]
do
	echo "*** NTP Service is not done. Please wait for a while."
	echo "*** Current time: `date`"
	echo "____ Time cost: $while_count min."
	echo "____ Sleep [sec.]: $sleep_sec"
	sleep $sleep_sec
	echo ""

	let while_count=while_count+1

done

echo "---- ntpstat:"
ntpstat
echo ""

echo "---- ntpq"
ntpq -p
echo ""

# 脚本结束
echo "%%%%%%%%%%% done: `date`"

# 结束
