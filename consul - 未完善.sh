服务端启动：

	备忘说明：
		安装：拷贝Consul到PATH中并给予"x"权限，在Unix中可直接使用，例：/usr/local/bin/consul
		完成安装后所有节点必须运行agent! agent可分为：server、client。每个数据中心至少须有1台consul -server #会成为集群中的Leader
		集群中其他agent运行为client。它是轻量级进程，主要负责注册服务、健康检查、转发对server的查询...
	
	启动示例：
		consul agent -server -rejoin -bootstrap-expect <Num> -data-dir /var/consul -node=<Name> -ui-dir <Path> -config-dir=/etc/consul.d/  -bind=<ip>  -client 0.0.0.0
		参数说明：
		-server		          使agent运行在server模式
		-rejoin		          忽略先前的离开、再次启动时仍尝试加入集群
		-bootstrap-expect 	  在1个"datacenter"中期望的server节点数，当该值提供时consul将一直等待达到指定的sever数量的时才会去引导整个集群（该标记不能和bootstrap共用）
		-bootstrap		  设置server是否为"bootstrap"模式。若数据中心只有1个server agent则需设置该参数。理论上处于bootstrap模式的server可以选择自己作为Raft Leader，集群中只有1个节点可配该参数
		-data-dir		  其为agent存放"元"数据，任何节点都必须有！。该目录应在持久存储中（reboot不丢失），对server角色的agent很关键：此时它要记录整个集群的state状态
		-node		          本节点在集群中的名称，在集群中它必须唯一，默认是该节点主机名，建议指定
		-ui-dir		          提供存放web ui资源的路径。该目录必须可读！
		-config-dir	          需加载的配置目录，里面所有以"json"结尾的文件都会被加载！表示node自身所注册的服务文件的存储路径（其中的子目录不会被加载、服务定义文件是注册服务的最通用的方式）
		-config-file	          需加载的配置文件，文件中都是"json"格式的信息，该参数可多次配置，后面文件中加载的参数会覆盖前面加载文件中的参数...?
		-bind		          该地址用于集群内部的通讯、集群内所有节点到此地址都必须是可达的，默认：0.0.0.0 （c/s都需设置，用于consul内部的通讯）
		-client		          将绑定到client接口的地址（即公开公开的地址），此地址提供HTTP、DNS、RPC服务。默认"127.0.0.1"，即只允许回路连接。RPC地址会被其他的consul命令使用，如：consul members查询 
		-log-level		  日志级别。默认"info"。有如下级别："trace","debug", "info", "warn",  "err"。可使用：consul monitor来连接agent查看日志
		-syslog			  将日志记录进syslog（仅支持Linux和OSX平台）
		-pid-file		  记录pid的文件
		-datacenter		  数据中心的名字，旧版本选项为：-dc
		
	配置示例：		 #即参数：-config-dir指定目录下的 ***.json （此方式可省去参数直接只用配置文件启动consul服务端）
		{  
			"datacenter": "east-aws",  		#同命令行参数-datacenter
			"data_dir": "/opt/consul",  		#同命令行参数-data_dir
			"log_level": "INFO",  			#同命令行参数-log_level
			"node_name": "foobar",  		#同命令行参数node
			"server": true,  
			"watches": [  
				{  
					"type": "checks",  
					"handler": "/usr/bin/health-check-handler.sh"  
				}  
			],  
			"telemetry": {  
				"statsite_address": "127.0.0.1:2180"  
			}  
		}
		
	查看成员：
		~]#  consul members
		Node  Address                     Status  Type    Build    Protocol  DC
		s1     10.201.102.198:8301  alive    server   0.7.4   2             dc1
		s2     10.201.102.199:8301  alive    server   0.7.4   2             dc1

---------------------------------------------------------------------------------------------------------------------

客户端启动：

	客户加入：
	consul agent -ui -data-dir /var/node1 -node=node1 -bind=192.168.11.144 -datacenter=dc1 -config-dir=/etc/consul.d/ -join 10.201.102.198
		备忘说明：
			参数："-ui" 启动内建界面，可通过形如："http://192.168.11.143:8500/ui/" 的形式访问
			参数："-join" 可使agent加入已有集群。 当agent以client模式运行时不加参数："server"就ok！
			后期加入集群："consul join <集群任意节点Ip地址>"	注：若报：Error joining the cluster: dial tcp 10.0.0.53:8301: getsockopt: no route to host 可能是防火墙的原因，检查端口8301是否开放
			重点：为加入集群，一个Consul的agent只需了解一个已存在的集群成员，加入集群后agent将会自动传递完整的consul成员信息......
			重启和移除节点：consul <reload/leave>			#服务定义可通过配置文件并发送SIGHUP给agent已进行更新
			参数："-client"指定了客户端接口的绑定地址，包括：HTTP、DNS、RPC，而consul join、members 都是通过RPC与Consul交互的		#例子：-rpc-addr=192.168.11.143:8400
				
	注册服务：
	备忘说明：
		搭建好conusl集群后，用户或程序就能到consul中去查询、注册服务。可通过两种方式注册服务：1）提供服务定义文件、2）调用HTTP API
		首先为consul创建配置目录，其会载入此目录的所有文件，在Unix中通常类似：/etc/consul.d。然后编写服务定义配置文件
		本例假设有名叫web的服务运行在80端口，另外给他设一个标签，这样可使用他作为额外的查询方式：......
	操作步骤：
		1、设定consul端配置文件：
			mkdir /etc/consul.d &&	echo '{"service": {"name": "web", "tags": ["rails"], "port": 80}}' > /etc/consul.d/web.json
			参数说明：
				name		服务名称
				port			服务端口
				tages		标签（自定义）
		2、重启client端服务：
				consul agent -server -bootstrap-expect 1 -data-dir /var/consul -node=s1 -bind=10.201.102.198 -rejoin -config-dir=/etc/consul.d/ -client 0.0.0.0
				备忘说明：
					参数："-data-dir"。提供目录来存放agent的状态，所有的agent都需要该目录并且该目录必须是稳定的（系统重启后都继续存在）
					若重启后输出："[INFO] agent: Synced service 'web'"，则说明此agent从配置文件中载入了服务定义并成功注册到服务目录......
					若需注册多个服务可在Consul配置目录创建多个服务定义文件......
						
	健康检查：			#在consul的配置目录：xxx.json。与服务类似，检查可以通过：1）检查定义、2）HTTP API请求。来注册......
	备忘说明：
		在基于脚本的健康检查中：脚本运行在与Consul进程同样的用户下，若此命令以非0值退出则此节点会被标记为不健康！这是所有基于脚本的健康检查的约定......
		每种check都须包含name！但：id、notes两个是可选的。若没提供id则id会被设为name。在一个节点中，check的ID必须唯一！因此若名字冲突那么ID就应设置......
		字段Notes主要是增强checks的可读性。Script check中"notes"字段可由脚本生成。同样，适用HTTP接口更新TTL check的外部程序一样可设置notes字段......
		Check脚本可自由地做任何事情确定check状态。唯一限制是退出代码必须遵循下面的约定：0-->正常、1-->告警、其他-->失败。Consul依赖此约定。脚本其他的输出都保存在notes字段中以供人查看
		注意，当我们尝试用DNS查询不健康的web服务时Consul将不会返回结果，因为服务不健康.....
		
	示例一：
		{  
			"check": {  
				"id": "mem-util",  
				"name": "Memoryutilization",  "script": "/usr/local/bin/check_mem.py",  "interval": "10s",  
				"timeout": "1s"  
			}  
		} 
	示例二：
		{  
			"check": {  
				"id": "api",  
				"name": "HTTPAPI on port 5000",  "http": "http://localhost:5000/health",  "interval": "10s",  
				"timeout": "1s"  
			}  
		} 
	示例三：
		{  
			"check": {  
				"id": "ssh",  
				"name": "SSHTCP on port 22",  "tcp": "localhost:22",  "interval": "10s",  
				"timeout": "1s"  
			}  
		}  
	示例四：
		{  
			"check": {  
				"id": "mem-util",  
				"name": "Memoryutilization",  
				"docker_container_id": "f972c95ebf0e",  
				"shell": "/bin/bash",  "script": "/usr/local/bin/check_mem.py",  
				"interval": "10s"  
			}  
		} 
	示例五：
		echo '{"check": {"name": "ping", "script": "ping -c1 163.com >/dev/null", "interval": "30s"}}'  >/etc/consul.d/ping.json
			
	检测健康：
		~]# curl http://localhost:8500/v1/health/state/critical		#注意:这个命令可以运行在任何节点！！~。critical指的类似于日志的级别......?
		[
			{
				"Node": "agent-two", 
				"CheckID": "service:web", 
				"Name": "Service 'web' check", 
				"Status": "critical", 
				"Notes": "", 
				"ServiceID": "web", 
				"ServiceName": "web"
			}
		]
	
	键值存储：
	为了提供服务发现及健康检测，Consul提供了非常容易使用的键/值对存储。它能被用于存储动态配置信息、帮助服务协作、建构Leader选举机制、及开发者可以想到的建构任何其它的东西
	
	这里展示了查询本地代理，我们先验证键值存储中有没有键存在：			#若查询不存在的key时将返回404错误
		curl -v http://localhost:8500/v1/kv/?recurse			#因不存在将会返回404错误......( 注：recurse即递归 )
	先用PUT方法存储一些键：
		curl -X PUT -d 'test' http://localhost:8500/v1/kv/web/key1				
		curl -X PUT -d 'test' http://localhost:8500/v1/kv/web/key2?flags=42		#其中：web/key2是键的名字、?flags键的标记信息（为64位的整行数字，可被客户端用来做一些元数据.）
		curl -X PUT -d 'test' http://localhost:8500/v1/kv/web/sub/key3
	查询存储的键：
			curl http://localhost:8500/v1/kv/?recurse
			[{"CreateIndex":97,"ModifyIndex":97,"Key":"web/key1","Flags":0,"Value":"dGVzdA=="},
			{"CreateIndex":98,"ModifyIndex":98,"Key":"web/key2","Flags":42,"Value":"dGVzdA=="},
			{"CreateIndex":99,"ModifyIndex":99,"Key":"web/sub/key3","Flags":0,"Value":"dGVzdA=="}]
		备忘说明：
		这里我们创建了3个键，每个都关联了值"test"。注意"值"字段的返回是基于base64的编码，该编码允许非UTF8字符集。对于键"web/key2"，我们为其设置了一个42的标记。
		所有的键都支持设置一个64位长的整形标记值。这个标记并不是由Consul内部使用的，它可被用于存储任意键值对的元数据信息。
		在设置值之后，我们使用 ?recurse 参数发出了GET请求来接收多个键的信息。
		 
		也可以非常容易地获取单个键的信息：
		curl http://localhost:8500/v1/kv/web/key1
		[{"CreateIndex":97,"ModifyIndex":97,"Key":"web/key1","Flags":0,"Value":"dGVzdA=="}]
		
		删除所有键：curl -X DELETE http://localhost:8500/v1/kv/web/sub?recurse			#此处删除了sub的所有值
		
		修改键：
			使用一个PUT请求相同的URI并且提供一个不同的消息体即可修改指定的键，Consul提供了一个检测并设置的操作，对应的操作是原子的......
			通过在GET请求中提供 ?cas= 参数以及指定最新的 ModifyIndex 值我们就可以得到原子CAS操作。例如，假设我们想要更新"web/key1"：
			curl -X PUT -d 'newval' http://localhost:8500/v1/kv/web/key1?cas=97			#返回true
			curl -X PUT -d 'newval' http://localhost:8500/v1/kv/web/key1?cas=97			#返回false
			这里，第一个CAS更新成功了因为最新的 ModifyIndex 是97，而第二个操作失败了因为最新的 ModifyIndex 不再是97了。
		
			curl "http://localhost:8500/v1/kv/web/key2?index=101&wait=5s"
			[{"CreateIndex":98,"ModifyIndex":101,"Key":"web/key2","Flags":42,"Value":"dGVzdA=="}]
			通过提供"?index="参数，我们请求等待直到键包含了一个大于101的 ModifyIndex 的值。无论如何由于"?wait=5"参数限制了查询最多等待5秒，之后会返回当前没有修改的值。
			该操作可以高效地等待键的更新。另外相同的方法可以用于等待一个键的集合，直到键集合中任何一个键发生的更新。
	
	停止客户端：
		说明：
			可用Ctrl-C 优雅的关闭Agent. 中断Agent之后你可以看到他离开了集群并关闭.
			在退出中,Consul提醒其他集群成员此节点离开了.若强行杀掉进程则集群其他成员应能检测到这个节点失效了.当一个成员离开,他的服务和检测也会从目录中移除
			当成员失效时他的健康状况被简单的标记为危险但不会从目录中移除，Consul会自动尝试对失效的节点重连等待并允许他从某些网络条件下恢复过来，而离开的节点则不会再继续联系.
			若一个agent作为一个服务器,一个优雅的离开是很重要的,可以避免引起潜在的可用性故障影响达成一致性协议.
------------------------------------------------------------------------------------------------------------
	
备忘：
通过member查看的是最终一致性，强一致性需要去server端查看：这里访问本地时将会自动转发至server端！：curl localhost:8500/v1/catalog/nodes
返回：
[{"Node":"hdp2","Address":"10.0.0.52","TaggedAddresses":{"wan":"10.0.0.52"},"CreateIndex":3,"ModifyIndex":4}]


	
		让我们首先使用DNS API来查询.在DNS API中,服务的DNS名字是 NAME.service.consul. 
		虽然是可配置的,但默认的所有DNS名字会都在consul命名空间下.这个子域告诉Consul,我们在查询服务,NAME则是服务的名称.
		对于我们上面注册的Web服务.它的域名是 web.service.consul :
		（NS API中节点名称结构为 NAME.node.consul或者NAME.node.DATACENTER.consul.如果数据中心名字省略,Consul只会查询本地数据中心.）
			
		[root@hdp2 consul.d]# dig @127.0.0.1 -p 8600 web.service.consul
		
		;  DiG 9.8.2rc1-RedHat-9.8.2-0.47.rc1.el6  @127.0.0.1 -p 8600 web.service.consul
		; (1 server found)
		;; global options: +cmd
		;; Got answer:
		;; - HEADER - opcode: QUERY, status: NOERROR, id: 46501
		;; flags: qr aa rd; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 0
		;; WARNING: recursion requested but not available
		
		;; QUESTION SECTION:
		;web.service.consul.           IN         A
		
		;; ANSWER SECTION:
		web.service.consul.        0          IN         A          10.0.0.52
		
		;; Query time: 0 msec
		;; SERVER: 127.0.0.1#8600(127.0.0.1)
		;; WHEN: Wed Aug 17 19:07:05 2016
		;; MSG SIZE  rcvd: 70
		如你所见,一个A记录返回了一个可用的服务所在的节点的IP地址.A记录只能设置为IP地址. 有也可用使用 DNS API 来接收包含 地址和端口的 SRV记录:

		[root@hdp2 ~]# dig @127.0.0.1 -p 8600 web.service.consul SRV
		
		;  DiG 9.8.2rc1-RedHat-9.8.2-0.47.rc1.el6  @127.0.0.1 -p 8600 web.service.consul SRV
		; (1 server found)
		;; global options: +cmd
		;; Got answer:
		;; -HEADER- opcode: QUERY, status: NOERROR, id: 33415
		;; flags: qr aa rd; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1
		;; WARNING: recursion requested but not available
		
		;; QUESTION SECTION:
		;web.service.consul.           IN         SRV
		
		;; ANSWER SECTION:
		web.service.consul.        0          IN         SRV        1 1 80 hdp2.node.dc1.consul.
		
		;; ADDITIONAL SECTION:
		hdp2.node.dc1.consul.      0          IN         A          10.0.0.52
		
		;; Query time: 1 msec
		;; SERVER: 127.0.0.1#8600(127.0.0.1)
		;; WHEN: Thu Aug 18 10:40:48 2016
		;; MSG SIZE  rcvd: 130
		SRV记录告诉我们 web 这个服务运行于节点hdp2.node.dc1.consul 的80端口. DNS额外返回了节点的A记录.
		
		我们也可以用 DNS API 通过标签来过滤服务.基于标签的服务查询格式为TAG.NAME.service.consul. 在下面的例子中,我们请求Consul返回有 rails标签的 web服务.我们成功获取了我们注册为这个标签的服务:+
		[root@hdp2 ~]# dig @127.0.0.1 -p 8600 rails.web.service.consul SRV
		
		;  DiG 9.8.2rc1-RedHat-9.8.2-0.47.rc1.el6@127.0.0.1 -p 8600 rails.web.service.consul SRV
		; (1 server found)
		;; global options: +cmd
		;; Got answer:
		;; -HEADER opcode: QUERY, status: NOERROR, id: 3517
		;; flags: qr aa rd; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1
		;; WARNING: recursion requested but not available
		
		;; QUESTION SECTION:
		;rails.web.service.consul.         IN         SRV
		
		;; ANSWER SECTION:
		rails.web.service.consul. 0        IN         SRV        1 1 80 hdp2.node.dc1.consul.
		
		;; ADDITIONAL SECTION:
		hdp2.node.dc1.consul.      0          IN         A          10.0.0.52
		
		;; Query time: 1 msec
		;; SERVER: 127.0.0.1#8600(127.0.0.1)
		;; WHEN: Thu Aug 18 11:26:17 2016
		;; MSG SIZE  rcvd: 142
		
		除了DNS API之外,HTTP API也可以用来进行服务查询:
		[root@hdp2 ~]# curl http://localhost:8500/v1/catalog/service/web
		[{"Node":"hdp2","Address":"10.0.0.52","ServiceID":"web","ServiceName":"web","ServiceTags":["rails"],"ServiceAddress":"","ServicePort":80,"ServiceEnableTagOverride":false,"CreateIndex":4,"ModifyIndex":254}]
		
		目录API给出所有节点提供的服务.稍后我们会像通常的那样带上健康检查进行查询.就像DNS内部处理的那样.这是只查看健康的实例的查询方法:
		[root@hdp2 ~]# curl http://localhost:8500/v1/catalog/service/web?passing
		[{"Node":"hdp2","Address":"10.0.0.52","ServiceID":"web","ServiceName":"web","ServiceTags":["rails"],"ServiceAddress":"","ServicePort":80,"ServiceEnableTagOverride":false,"CreateIndex":4,"ModifyIndex":254}]

		
-ui：
Consul同时提供了一个漂亮的功能齐全的WEB界面,开箱即用.界面可以用来查看所有的节点,可以查看健康检查和他们的当前状态.可以读取和设置K/V 存储的数据.UI自动支持多数据中心.




模板：关于模板的官方说明：https://github.com/hashicorp/consul-template
Consul Template 提供一个方便的方式从Consul获取数据通过consul-template的后台程序保存到文件系统.
consul-template会通过Http请求从Consul中读取集群中的数据，数据发生变更时 consul-template会触发更新指定配置文件的操作。
这个后台进程监控Consul示例的变化并更新任意数量的模板到文件系统.作为一个附件功能,模板更新完成后consul-template可以运行任何命令.
注意！这个模板的功能可能需要单独的去安装...（也是仅一个文件！） 继承了consul的风格，consul-template下载下来解压后就是一个二进制文件，没有其他多余的内容
consul-template提供了一个便捷的方式从consul中获取存储的值，consul-template守护进程会查询consul实例，来更新系统上指定的任何模板，当更新完成后，模板可以选择运行一些任意的命令。
 template内制静止平衡功能，可以智能的发现consul实例中的更改信息。这个功能可以防止频繁的更新模板而引起系统的波动。
 dry mode：不确定当前架构的状态？担心模板的变化会破坏子系统？无须担心，因为consul template还有-dry模式。在dry模式，consul template会将结果呈现在STDOUT，所以操作员可以检查输出是否正常，以决定更换模板是否安全

它的参数：
	-auth=<user[:pass]>      设置基本的认证用户名和密码
	-consul=<address>        设置Consul实例的地址
	-max-stale=<duration>    查询过期的最大频率，默认是1s
	-dedup                   启用重复数据删除，当许多consul template实例渲染一个模板的时候可以降低consul的负载
	-ssl                     使用https连接Consul使用SSL
	-ssl-verify              通过SSL连接的时候检查证书
	-ssl-cert                SSL客户端证书发送给服务器
	-ssl-key                 客户端认证时使用的SSL/TLS私钥
	-ssl-ca-cert             验证服务器的CA证书列表
	-token=<token>           设置Consul API的token
	-syslog                  把标准输出和标准错误重定向到syslog，syslog的默认级别是local0。
	-syslog-facility=<f>     设置syslog级别，默认是local0，必须和-syslog配合使用
	-template=<template>     增加一个需要监控的模板，格式是：'templatePath:outputPath(:command)'，多个模板则可以设置多次
	-wait=<duration>         当呈现一个新的模板到系统和触发一个命令的时候，等待的最大最小时间。如果最大值被忽略，默认是最小值的4倍。
	-retry=<duration>        当在和consul api交互的返回值是error的时候，等待的时间，默认是5s。
	-config=<path>           配置文件或者配置目录的路径
	-pid-file=<path>         PID文件的路径
	-log-level=<level>       设置日志级别，可以是"debug","info", "warn" (default), and "err"
	-dry                     Dump生成的模板到标准输出，不会生成到磁盘
	-once                    运行consul-template一次后退出，不以守护进程运行
	-reap                    子进程自动收割
 

查询 ```demo.consul.io``` 这个 ```Consul```实例(agent).渲染模板文件 ```/tmp/template.ctmpl``` 保存到 ``` /tmp/result```, 运行```Consul-template``` 服务直到直到手动结束:
consul-template  -consul demo.consul.io  -template "/tmp/template.ctmpl:/tmp/result"+


查询本地的```Consul```实例(agent),一旦模板发生变化渲染模板并重启```Nginx```,如果```Consul```不可用30秒重试一次:
consul-template  -consul 127.0.0.1:8500  -template "/tmp/template.ctmpl:/var/www/nginx.conf:service nginx restart"  -retry 30s  -once

查询一个```Consul```实例,渲染多个模板并作为服务直到停止:
consul-template  -consul my.consul.internal:6124 \
 -template "/tmp/nginx.ctmpl:/var/nginx/nginx.conf:service nginx restart" \
 -template "/tmp/redis.ctmpl:/var/redis/redis.conf:service redis restart" \
 -template "/tmp/haproxy.ctmpl:/var/haproxy/haproxy.conf"

查询一个需要权限验证的```Consul```实例,将渲染后的模板输出到控制台而不写入磁盘.
在这个例子中```-template```的第二个和第三个参数是必须的但是被忽略了.这个文件将不会被写入磁盘,命令也不会被执行.
consul-template  -consul my.consul.internal:6124  -template "/tmp/template.ctmpl:/tmp/result:service nginx restart" -dry

使用SSL证书进行```Consul```的查询:
consul-template  -consul 127.0.0.1:8543  -ssl  -ssl-cert /path/to/client/cert.pem \ 
-ssl-ca-cert /path/to/ca/cert.pem  -template "/tmp/template.ctmpl:/tmp/result"  -dry  -once

查询```Consul```并启动一个子进程.模板的变化会发送指令给子进程.详细的说明请查看[这里](https://github.com/hashicorp/consul-template#exec-mode).
consul-template  -template "/tmp/in.ctmpl:/tmp/result"  -exec "/sbin/my-server"


简单示例！：
说明：consul 是系统自带的服务 sonarqube 是我创建的服务。该服务的配置文件sonarqube.json 内容如下
	{
		"service": {
			"name": "sonarqube",
			"tags": ["dev"],
			"address":"www.163.com",
			"port": 80,
			"checks":[
				{
					"http":"http://www.163.com",
					"interval":"5s"
				}
			]
		}
	}

tmpltest.ctmpl内容：
	{{range services}}
	{{.Name}}
	{{range .Tags}}
	{{.}}{{end}}
	{{end}}

执行：consul-template.exe -consul 192.168.5.156:8500 -template "./tmpl/tmpltest.ctmpl:./tmpl/result"
	命令说明：
	-consul后是consul的webui接口 ，用web管理consul就用的8500端口。
	-template 后面是模板参数 第一个是模板地址 。冒号后的第二个参数是输出位置。
	
结果：
	consul
	sonarqube
	dev


-template 的参数 除了输入输出参数 还可以添加其他命令 如
E:\consul321>consul-template.exe -consul 192.168.5.156:8500 -template "./tmpl/tmpltest.ctmpl:./tmpl/result:service nginx restart"
	表示输出后 重启nginx服务
	-config 模板配置文件的路径
	-dry 模板内容不写入磁盘，写到控制台
	-log-level 日志级别 通常是info warn之类
	-max-stale 默认1秒，设置后，consul会把任务分发给各个server，而不是有leader独自完成。
	-once 运行一次后退出
	-pid-file 写模板文件的pid的信息保存的路径
	-ssl 和consul使用ssl通信 相关的有ssl-ca-cert ssl-cert ssl-verify
	-token consul的api token。没有默认值
	-version 版本
	除了consul和template 其他参数都是可选的



再来个例子
$ consul-template \
-consul 127.0.0.1:8500 \
-template "/tmp/template.ctmpl:/var/www/nginx.conf:service nginx restart" \
-retry 30s \
-once
表示如果consul有问题的话，每30秒轮询一次。

来个证书的命令的例子
$ consul-template \
-consul 127.0.0.1:8543 \
-ssl \
-ssl-cert /path/to/client/cert.pem \
-ssl-ca-cert /path/to/ca/cert.pem \
-template "/tmp/template.ctmpl:/tmp/result" \
-dry \
-once


模板的配置文件
例如创建一个tmpl.json文件
内容如下
	consul = "127.0.0.1:8500"
	template {
	source = "/etc/haproxy/haproxy.ctmpl"
	destination = "/etc/haproxy/haproxy.cfg"
	command = "service haproxy restart"
	}

接下来 我们就可以这样执行了
	consul-template -config /data/cfg/consul/tmpl.json

如果有多个模板要执行的话，可以这样，配多个template参数就行了
	consul-template \
	-consul my.consul.internal:6124 \
	-template "/tmp/nginx.ctmpl:/var/nginx/nginx.conf:service nginx restart" \
	-template "/tmp/redis.ctmpl:/var/redis/redis.conf:service redis restart" \
	-template "/tmp/haproxy.ctmpl:/var/haproxy/haproxy.conf"
	
查询本地consl实例，生成模板后重启nginx，如果consul不可用，如果api故障则每30s尝试检测一次值，consul-template运行一次后退出
consul-template \
  -consul 127.0.0.1:8500 \
  -template "/tmp/template.ctmpl:/var/www/nginx.conf:service nginx restart" \
  -retry 30s \
  -once

查询一个实例，渲染多个模板，然后重启相关服务
consul-template \
  -consul my.consul.internal:6124 \
  -template "/tmp/nginx.ctmpl:/var/nginx/nginx.conf:service nginx restart" \
  -template "/tmp/redis.ctmpl:/var/redis/redis.conf:service redis restart" \
  -template "/tmp/haproxy.ctmpl:/var/haproxy/haproxy.conf"
  
查询一个实例，dump模板到标准输出，参数中的-template则会被忽略
consul-template \
  -consul my.consul.internal:6124 \
  -template "/tmp/template.ctmpl:/tmp/result:service nginx restart"
  -dry
  

  
Consul-Template的配置文件，简称HCL(HashiCorp Configuration Language)，它是和JSON兼容的，下面看个例子：
consul = "127.0.0.1:8500"
token = "abcd1234"
retry = "10s"
max_stale = "10m"
log_level = "warn"
pid_file = "/path/to/pid"
wait = "5s:10s"

vault {
  address = "https://vault.service.consul:8200"
  token = "abcd1234"
  renew = true
  ssl {
    // ...
  }
}

auth {
  enabled  = true
  username = "test"
  password = "test"
}

ssl {
  enabled = true
  verify = false
  cert = "/path/to/client/cert"
  key = "/path/to/client/key"
  ca_cert = "/path/to/ca"
}


syslog {
  enabled = true
  facility = "LOCAL5"
}


deduplicate {

  enabled = true
  prefix = "consul-template/dedup/"
}


template {
  source = "/path/on/disk/to/template.ctmpl"
  destination = "/path/on/disk/where/template/will/render.txt"
  command = "restart service foo"
  command_timeout = "60s"
  perms = 0600
  backup = true
  left_delimiter  = "{{"
  right_delimiter = "}}"
  wait = "2s:6s"
}

 以上并不是所有的fields都需要，比如Vault你可能就不需要，所以你就不需要指定Vault配置。以上就是配置文件。

 
例子：
		[Jack@n36 ~]$ curl -s 10.111.222.35:8500/v1/catalog/service/webapp |python -mjson.tool
		[
			{
				"Address": "10.111.222.36",
				"Node": "0db39e28b326",
				"ServiceAddress": "",
				"ID": "1f61c2d2bcf9:z001:5000",
				"Name": "webapp",
				"Port": 32774,
				"Tags": null
			},
			{
				"Address": "10.111.222.35",
				"Node": "be67d37cbf68",
				"ServiceAddress": "",
				"ID": "205155915c61:z002:5000",
				"Name": "webapp",
				"Port": 32768,
				"Tags": null
			}
		]
		【---------】
		[root@localhost ~]# cat consul.ctmpl 
		{{range service "webapp"}}
		server {{.Address}}:{{.Port}}
		{{end}}
		【---------】
		渲染后：
		[Jack@n36 ~]$ cat /tmp/consul.result
		
		server 10.111.222.36:32774
		server 10.111.222.35:32768
		
----------------------------------------------------
调整 haproxy 模版：
[root@n36 ~]# vim /etc/haproxy/haproxy.cfg.ctmpl
（略）
backend app
    balance     roundrobin
    {{range service "webapp"}}
    server app-{{.Port}} {{.Address}}:{{.Port}} check
	{{end}}	
		
验证配置：
[root@n36 ~]# cat /etc/haproxy/haproxy.cfg
（略）
backend app
    balance     roundrobin
     
    server app-32774 10.111.222.36:32774 check
    server app-32775 10.111.222.36:32775 check
    server app-32776 10.111.222.36:32776 check
----------------------------------------------------
docker的consul注意事项：
	-bootstrap-expect 3：表明需要有3个节点，才能启动集群。
	-bootstrap：单个节点使用这个标记来立即启动服务，而不是用来等待集群的创建。
	-advertise：来申明 consul 使用哪个 IP 来提供服务。
	-join：指定第一个 consul 服务的 IP 来加入集群。


	
	查询指定的key值：{{key“service / redis / maxconns”}}	输出：15
	
	
	如果key不存在则，存在则...：
	{{if keyExists“app / beta_active”}}
	＃...
	{{else}}
	＃...
	{{ 结束 }}
	
	在给定的键路径上查询所有顶级kv对的领事。
	{{ls“<PATH> @ <DATACENTER>”}}
	例如：
	{{range ls“service / redis”}} 
	{{.Key}}：{{.Value}} {{end}}
	呈现
	maxconns:15
	minconns:5
	
	的<NAME>属性是可选的; 如果省略，则使用本地代理节点。
	的<DATACENTER>属性是可选的; 如果省略，则使用本地数据中心。
	
	{{with node}} 
	{{.Node.Address}} {{end}}
	输出：10.5.2.6
	
	查询不同的节点：
	{{with node“node1 @ dc2”}} 
	{{.Node.Address}} {{end}}
	输出：10.4.2.6
	
	{{range nodes}} 
	{{.Address}}
	{{end}}
	输出：
	10.4.2.13
	10.46.2.5
	
	接受base64编码的字符串并返回解码的结果，如果给定的字符串不是有效的base64字符串，则返回错误。
	{{base64Decode“aGVsbG8 =”}}
	输出：hello
	
