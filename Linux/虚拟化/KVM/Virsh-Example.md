#### 查看所有虚拟机
`virsh list --all`
#### 查看运行的虚拟机
`virsh list`  
虚拟机的状态有 8 种  
* runing  运行状态     
* idel    空闲状态   
* pause   停状态 
* shutdown 关闭状态   
* crash   虚拟机崩坏状态   
* daying  垂死状态   
* shut off  不运行完全关闭   
* pmsuspended   客户机被关掉电源中中断  

#### 列出所有的块设备
`virsh domblklist 实例名`  

#### 列出虚拟机的所有网口：  
`virsh domiflist 实例名`    
```
Interface  Type       Source     Model       MAC  
-------------------------------------------------------  
vnet0      bridge     br0      virtio      52:54:10:e6:c9:02  
vnet1      bridge     br1      virtio      52:54:10:f5:c5:6c  
```
#### 新增一个网口
`virsh attach-interface 实例名 --type bridge --source br1 --model virtio --config `         // 下次启动生效    
`virsh attach-interface 实例名 --type bridge --source br1 --model virtio --current`         // 立即生效    
`virsh detach-interface 实例名 --type bridge --mac 52:54:10:f5:c5:6c --config     `         // 下次启动生效    
`virsh detach-interface 实例名 --type bridge --mac 52:54:10:f5:c5:6c --current    `         // 立即生效    

#### 关闭或打开某个网口
`virsh domif-setlink 实例名 vnet0 down`    
`virsh domif-setlink 实例名 vnet0 up`  
 
#### 获取某个网口状态  
`virsh domif-getlink 实例名 vnet1`  
 
#### 设置虚拟机自启动
`virsh autostart 实例名`  
 
#### 虚拟机的启动，关闭，重启，创建，查看VNC，链接虚拟机，启动并进入虚拟机
`virsh start 实例名`  
`virsh shutdown 实例名`  
`virsh reboot 实例名`
`virsh define demo.xml`  
`virsh vncdisplay 实例名`
`virsh console 实例名` 退出虚拟机用 ：ctrl+]  
`virsh start 实例名 --console`

#### 虚拟机的挂起和恢复
`virsh suspend 实例名`  
`virsh resume 实例名`  
#### 彻底删除虚拟机
`virsh destroy 实例名` 删除虚拟机  
`virsh undefine 实例名` 解除标记  

#### 子机随宿主主机（母机）启动而启动
`virsh autostart 实例名`
`virsh auotstart --disable 实例名`  取消自启  
