#### 参数
```txt
%F      即：yyyy-mm-dd（+%Y-%m-%d）
%y      年份的最后两位数字 (00.99)
%Y      完整年份 (0000-9999)
%m      月份 (01-12)
%d      日 (01-31)
%H      小时(00-23)
%M      分钟(00-59)
%S      秒(00-60)
%b      月份 (Jan-Dec)
%B      月份 (January-December)
%D      直接显示日期 (mm/dd/yy)
%T      直接显示时间 (24 小时制)
%h      同 %b
%n      下一行
%t      跳格
%I      小时(01-12)
%k      小时(0-23)
%l      小时(1-12)
%p      显示本地 AM 或 PM
%r      直接显示时间 (12 小时制，格式为 hh:mm:ss [AP]M)
%s      从 1970 年 1 月 1 日 00:00:00 UTC 到目前为止的秒数
%X      相当于 %H:%M:%S
%Z      显示时区
%a      星期几 (Sun-Sat)
%A      星期几 (Sunday-Saturday)
%c      直接显示日期与时间
%j      一年中的第几天 (001-366)
%U      一年中的第几周 (00-53) (以 Sunday 为一周的第一天的情形)
%w      一周中的第几天 (0-6)
%W      一年中的第几周 (00-53) (以 Monday 为一周的第一天的情形)
%x      直接显示日期 (mm/dd/yy)
%N      纳秒

```
#### Example
```bash
[root@localhost tmp]# date "+now time: %y-%m-%d %H:%M:%S" 
now time: 17-08-15 22:24:36
[root@localhost tmp]# date "+三年前的此刻是: %y-%m-%d %H:%M:%S" -d "-3 years"
三年前的此刻是: 14-08-15 22:25:52
[root@localhost tmp]# date "+三个月后时间是: %y-%m-%d %H:%M:%S" -d "+3 months"               
三个月后时间是: 17-11-15 22:26:38
[root@localhost tmp]# date "+十天之后时间是: %y-%m-%d %H:%M:%S" -d "+10 days"       
十天之后时间是: 17-08-25 22:27:22

#设置系统时间的几个例子（date足够智能）
[root@localhost tmp]# date -s "20171027 20:49:30"
2017年 10月 27日 星期五 20:49:30 CST
[root@localhost tmp]# date -s "20:49:30 20171027"
2017年 10月 27日 星期五 20:49:30 CST
[root@localhost tmp]# date -s "20:49:30 2017/10/27"
2017年 10月 27日 星期五 20:49:30 CST
[root@localhost tmp]# date -s "20:49:30 2017-10-27"
2017年 10月 27日 星期五 20:49:30 CST

#一年中的第几天
[root@localhost tmp]# date "+%j"
300

#偷懒的方法
[root@localhost tmp]# date "+%F %T"
2017-10-27 20:52:33
```
