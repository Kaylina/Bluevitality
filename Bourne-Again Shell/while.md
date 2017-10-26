#### Example
```
#使用IFS指定输入分隔符！相当于awk中的-F或FS变量
[root@localhost ~]# while IFS=: read name pass uid gid fullname homedir shell
> do
> echo $name
> done < /etc/passwd
root
bin
daemon
adm
lp
sync
shutdown
halt
mail
operator
games
ftp
nobody
avahi-autoipd
systemd-bus-proxy
systemd-network
dbus
polkitd
apache
abrt
libstoragemgmt
postfix
pcp
tss
chrony
sshd
ntp
tcpdump
oprofile
rpc
```
