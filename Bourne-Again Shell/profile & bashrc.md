#### 说明
```txt
/etc/profile:     为系统每个用户设置环境信息，当用户第1次登录时该文件被执行.并从/etc/profile.d目录的配置文件中执行相关设置

/etc/bashrc:      为每个运行bash shell的用户执行此文件，当bash shell被打开时该文件被读取

~/.bash_profile:  每个用户都可使用该文件输入专用于自己的shell信息，当用户登录时该文件仅执行一次!
                  ~/.bash_profile 是交互式、login 方式进入bash 运行的；
                  默认用于设置环境变量并执行用户的.bashrc
                  此文件类似于/etc/profile，也需要重启生效
                  /etc/profile    对所有用户生效
                  ~/.bash_profile 对当前用户生效
                  
~/.bashrc:        包含专用于你的bash shell的bash信息，当登录及每次打开新的shell时该文件被读取!
                  ~/.bashrc 是交互式 non-login 方式进入bash 运行的；
                  类似于/etc/bashrc，不需要重启生效，重新打开一个bash即可生效
                  /etc/bashrc     对所有用户新打开的bash都生效，另外/etc/profile中设定的变量(全局)可以作用于任何用户
                  ~/.bashrc       只对当前用户新打开的bash生效，设定的变量(局部)只继承/etc/profile，他们是"父子"关系

~/.bash_logout:   当每次退出系统(退出bash shell)时执行该文件
```







