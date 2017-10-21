# nginx配置详解
------
### 1 序言
Nginx功能丰富，可作为HTTP服务器，也可做为反向代理服务器，邮件服务器。支持FastCGI、SSL、Virtual Host、URL Rewrite、Gzip等功能。并且支持很多第三方的模块扩展。
Nginx的稳定性、功能集、示例配置文件和低系统资源的消耗让他后来者居上，在全球活跃的网站中有12.18%的使用比率，大约为2220万个网站。
### 2 Nginx常用功能
###### 1、Http代理，反向代理:作为web服务器最常用的功能之一，尤其是反向代理
这里用两张图，对正向代理和反向代理做了个诠释，具体细节，大家可以翻阅以下资料。

![picture2-1](http://images2015.cnblogs.com/blog/398358/201602/398358-20160202133724350-1807373891.jpg)  

Nginx在做反向代理时，提供性能稳定，并且能够提供配置灵活的转发功能。Nginx可以根据不同的正则匹配，采取不同的转发策略，比如图片文件结尾的走文件服务器，动态页面走web服务器，只要正则写的没有问题，又有相对应的服务器解决方案，你就可以随心所欲的玩。并且对返回结果进行错误页面跳转，异常判断等。如果被分发的服务器存在异常，他可以将请求重新转发给另外一台服务器，然后自动去除异常服务器。
###### 2、负载均衡
Nginx提供的负载均衡策略有两种：内置策略和扩展策略。内置策略为轮询，加权轮询，IP hash。扩展策略，就天马行空，只有你想不到的没有他做不到的，你可以参照所有的负载均衡算法，给他一一找出来做下实现。  
上3个图，理解这三种负载均衡算法的实现

![picture2-2-1](http://images2015.cnblogs.com/blog/398358/201602/398358-20160202133753382-1863657242.jpg)

IP hash算法，对客户端的ip进行hash操作，然后根据hash结果将同一个客户端ip的请求分发给同一台服务器进行处理，可以解决session不共享的问题。

![picture2-2-2](http://images2015.cnblogs.com/blog/398358/201602/398358-20160201162405944-676557632.jpg)

###### 3、web缓存
Nginx可以对不同的文件做不同的缓存处理，配置灵活，并且支持FastCGI_Cache,主要用于对FastCGI的动态程序进行缓存。配合着第三方的ngx_cache_purge,对制定的URL缓存内容可以进行增删管理。
###### 4、Nginx相关资料地址
源码：[https://trac.nginx.org/nginx/browser](https://trac.nginx.org/nginx/browser)

官网：[http://www.nginx.org/](http://www.nginx.org/)
### 3、Nginx配置文件结构
如果你下载好，打开你的安装文件中conf文件夹下的nginx.conf文件，Nginx服务器的基础配置，默认的配置也存放在此。
在nginx.conf中的注释符号是**"#"**
nginx安装后的cofig配置如下
```
#user  nobody;
worker_processes  1;

#error_log  logs/error.log;
#error_log  logs/error.log  notice;
#error_log  logs/error.log  info;

#pid        logs/nginx.pid;


events {
    worker_connections  1024;
}


http {
    include       mime.types;
    default_type  application/octet-stream;

    #log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
    #                  '$status $body_bytes_sent "$http_referer" '
    #                  '"$http_user_agent" "$http_x_forwarded_for"';

    #access_log  logs/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    #keepalive_timeout  0;
    keepalive_timeout  65;

    #gzip  on;

    server {
        listen       80;
        server_name  localhost;

        #charset koi8-r;

        #access_log  logs/host.access.log  main;

        location / {
            root   html;
            index  index.html index.htm;
        }

        #error_page  404              /404.html;

        # redirect server error pages to the static page /50x.html
        #
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }

        # proxy the PHP scripts to Apache listening on 127.0.0.1:80
        #
        #location ~ \.php$ {
        #    proxy_pass   http://127.0.0.1;
        #}

        # pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
        #
        #location ~ \.php$ {
        #    root           html;
        #    fastcgi_pass   127.0.0.1:9000;
        #    fastcgi_index  index.php;
        #    fastcgi_param  SCRIPT_FILENAME  /scripts$fastcgi_script_name;
        #    include        fastcgi_params;
        #}

        # deny access to .htaccess files, if Apache's document root
        # concurs with nginx's one
        #
        #location ~ /\.ht {
        #    deny  all;
        #}
    }


    # another virtual host using mix of IP-, name-, and port-based configuration
    #
    #server {
    #    listen       8000;
    #    listen       somename:8080;
    #    server_name  somename  alias  another.alias;

    #    location / {
    #        root   html;
    #        index  index.html index.htm;
    #    }
    #}


    # HTTPS server
    #
    #server {
    #    listen       443 ssl;
    #    server_name  localhost;

    #    ssl_certificate      cert.pem;
    #    ssl_certificate_key  cert.key;

    #    ssl_session_cache    shared:SSL:1m;
    #    ssl_session_timeout  5m;

    #    ssl_ciphers  HIGH:!aNULL:!MD5;
    #    ssl_prefer_server_ciphers  on;

    #    location / {
    #        root   html;
    #        index  index.html index.htm;
    #    }
    #}

}
```
nginx文件结构
```
...              #全局块

events {         #events块
   ...
}

http      #http块
{
    ...   #http全局块
    server        #server块
    {
        ...       #server全局块
        location [PATTERN]   #location块
        {
            ...
        }
        location [PATTERN]
        {
            ...
        }
    }
    server
    {
      ...
    }
    ...     #http全局块
}
```
1、全局块：配置影响nginx全局的指令。一版有运行nginx服务器的用户组，nginx进程pid存放路径，日志存放路径，配置文件的引入，允许生成worker process数等。
2、event块：配置影响nginx服务器或用户的网络连接。有每个进程的最大连接数，选取哪种事件驱动模型处理连接请求，是否允许同时接受多个网络连接，开启多个网络连接序列化等。
3、http块：可以嵌套多个server,配置代理，缓存，日志定义等绝大多数功能和第三方模块的配置。如文件引入，mime-type定义，日志自定义，是否使用sendfile传输文件，连接超时时间，单连接请求数等。
4、server块：配置虚拟主机的相关参数，一个http中可以有多个server。
5、location块：配置请求的路由，以及各种页面的处理情况。
下面给大家上一个配置文件，作为理解。
```
########### 每个指令必须有分号结束。#################
#user administrator administrators;  #配置用户或者组，默认为nobody nobody。
#worker_processes 2;  #允许生成的进程数，默认为1
#pid /nginx/pid/nginx.pid;   #指定nginx进程运行文件存放地址
error_log log/error.log debug;  #制定日志路径，级别。这个设置可以放入全局块，http块，server块，级别以此为：debug|info|notice|warn|error|crit|alert|emerg
events {
    accept_mutex on;   #设置网路连接序列化，防止惊群现象发生，默认为on
    multi_accept on;  #设置一个进程是否同时接受多个网络连接，默认为off
    #use epoll;      #事件驱动模型，select|poll|kqueue|epoll|resig|/dev/poll|eventport
    worker_connections  1024;    #最大连接数，默认为512
}
http {
    include       mime.types;   #文件扩展名与文件类型映射表
    default_type  application/octet-stream; #默认文件类型，默认为text/plain
    #access_log off; #取消服务日志
    log_format myFormat '$remote_addr–$remote_user [$time_local] $request $status $body_bytes_sent $http_referer $http_user_agent $http_x_forwarded_for'; #自定义格式
    access_log log/access.log myFormat;  #combined为日志格式的默认值
    sendfile on;   #允许sendfile方式传输文件，默认为off，可以在http块，server块，location块。
    sendfile_max_chunk 100k;  #每个进程每次调用传输数量不能大于设定的值，默认为0，即不设上限。
    keepalive_timeout 65;  #连接超时时间，默认为75s，可以在http，server，location块。

    upstream mysvr {
      server 127.0.0.1:7878;
      server 192.168.10.121:3333 backup;  #热备
    }
    error_page 404 https://www.baidu.com; #错误页
    server {
        keepalive_requests 120; #单连接请求上限次数。
        listen       4545;   #监听端口
        server_name  127.0.0.1;   #监听地址
        location  ~*^.+$ {       #请求的url过滤，正则匹配，~为区分大小写，~*为不区分大小写。
           #root path;  #根目录
           #index vv.txt;  #设置默认页
           proxy_pass  http://mysvr;  #请求转向mysvr 定义的服务器列表
           deny 127.0.0.1;  #拒绝的ip
           allow 172.18.5.54; #允许的ip
        }
    }
}
```
上面是nginx的基本配置，需要注意的有以下几点：
    1.$remote_addr 与 $http_x_forwarded_for 用以记录客户端的ip地址；
    2.$remote_user:用来记录客户端用户的名称；
    3.$time_local:用来记录访问时间和时区；
    4.$request:用来记录请求的url和http协议；
    5.$status:用来记录请求状态；成功是200
    6.$body_bytes_s ent :记录发送给客户端文件主体内容大小；
    7.$http_referer:用来记录从哪个页面链接访问过来的；
    8.$http_user_agent:记录客户端浏览器的相关信息；
### 4、Nginx代理服务的配置说明
###### 1、在http模块中有下面的配置，当代理遇到状态码为404时，我们把404页面导向百度。
```
error_page 404 https://www.baidu.com; #错误页
```
然而要想这个配置起作用，我们必须配合下面的配置一起起作用
```
proxy_intercept_errors on;    #如果被代理服务器返回的状态码为400或者大于400，设置的error_page配置起作用。默认为off。
```
###### 2、如果我们的代理只允许接受get、post请求方式的一种可以参考一下配置
```
proxy_method get;    #支持客户端的请求方法。post/get；
```
###### 3、设置支持的http协议版本
```
proxy_http_version 1.0 ; #Nginx服务器提供代理服务的http协议版本1.0，1.1，默认设置为1.0版本
```
###### 4、如果你的nginx服务器给2台web服务器做代理，负载均衡算法采用轮询，那么当你的一台机器web应用关闭，也就是说web不能访问，那么Nginx服务器分发请求还是会给这台不能访问的web服务器，如果这里的响应连接时间过长，就会导致客户端的页面一直在等待响应，对用户来说体验就大打折扣，这里我们怎么避免这样的情况发生呢。请看以下配图。  

![picture4-4](http://images2015.cnblogs.com/blog/398358/201602/398358-20160219104130363-660910928.jpg)

如果负载均衡中其中web2发生这样的情况，nginx首先会去web1请求，但是nginx在配置不当的情况下会继续分发请求到web2,然后等待web2响应，直到我们的响应时间超时，才会把请求重新分发给web1，这里的响应时间如果过长，用户等待的时间就会越长。
下面的配置是解决方案之一。
```
proxy_connect_timeout 1;   #nginx服务器与被代理的服务器建立连接的超时时间，默认60秒
proxy_read_timeout 1; #nginx服务器想被代理服务器组发出read请求后，等待响应的超时间，默认为60秒。
proxy_send_timeout 1; #nginx服务器想被代理服务器组发出write请求后，等待响应的超时间，默认为60秒。
proxy_ignore_client_abort on;  #客户端断网时，nginx服务器是否终端对被代理服务器的请求。默认为off。
```
###### 5、如果使用upstream指令配置了一组服务器作为被代理服务器，服务器中的访问算法遵循配置的负载均衡规则，同时可以使用该指令配置在发生哪些异常情况时，将请求顺次交由下一组服务器处理。
```
proxy_next_upstream timeout;  #反向代理upstream中设置的服务器组，出现故障时，被代理服务器返回的状态值。error|timeout|invalid_header|http_500|http_502|http_503|http_504|http_404|off
```
error:建立连接或向被代理的服务器发送请求或读取响应信息时服务器发生错误。
timeout:建立连接，想被代理服务器发送请求或读取响应信息时服务器发生超时。
invalid_header:被代理服务器返回的响应头异常。
off:无法将请求分发给被代理的服务器。
http_404,....:被代理服务器返回的状态码为404,500，等。
###### 6、如果你想通过http获取客户的真实ip而不是获取代理服务器的ip地址，那么要做如下的设置。
```
proxy_set_header Host $host; #只要用户在浏览器中访问的域名绑定了 VIP VIP 下面有RS；则就用$host ；host是访问URL中的域名和端口  www.taobao.com:80
proxy_set_header X-Real-IP $remote_addr;  #把源IP 【$remote_addr,建立HTTP连接header里面的信息】赋值给X-Real-IP;这样在代码中 $X-Real-IP来获取 源IP
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;#在nginx 作为代理服务器时，设置的IP列表，会把经过的机器ip，代理机器ip都记录下来，用 【，】隔开；代码中用 echo $x-forwarded-for |awk -F, '{print $1}' 来作为源IP
```
关于X-Forwarded-For与X-Real-IP的一些相关文章我推荐一位大神的:[HTTP请求头中的X-Forwarded-For](),这位大神对http协议有一系列的文章阐述。  
###### 7、下面是我的一个关于代理配置的配置文件部分，仅供参考。  
```
    include       mime.types;   #文件扩展名与文件类型映射表
    default_type  application/octet-stream; #默认文件类型，默认为text/plain
    #access_log off; #取消服务日志    
    log_format myFormat ' $remote_addr–$remote_user [$time_local] $request $status $body_bytes_sent $http_referer $http_user_agent $http_x_forwarded_for'; #自定义格式
    access_log log/access.log myFormat;  #combined为日志格式的默认值
    sendfile on;   #允许sendfile方式传输文件，默认为off，可以在http块，server块，location块。
    sendfile_max_chunk 100k;  #每个进程每次调用传输数量不能大于设定的值，默认为0，即不设上限。
    keepalive_timeout 65;  #连接超时时间，默认为75s，可以在http，server，location块。
    proxy_connect_timeout 1;   #nginx服务器与被代理的服务器建立连接的超时时间，默认60秒
    proxy_read_timeout 1; #nginx服务器想被代理服务器组发出read请求后，等待响应的超时间，默认为60秒。
    proxy_send_timeout 1; #nginx服务器想被代理服务器组发出write请求后，等待响应的超时间，默认为60秒。
    proxy_http_version 1.0 ; #Nginx服务器提供代理服务的http协议版本1.0，1.1，默认设置为1.0版本。
    #proxy_method get;    #支持客户端的请求方法。post/get；
    proxy_ignore_client_abort on;  #客户端断网时，nginx服务器是否终端对被代理服务器的请求。默认为off。
    proxy_ignore_headers "Expires" "Set-Cookie";  #Nginx服务器不处理设置的http相应投中的头域，这里空格隔开可以设置多个。
    proxy_intercept_errors on;    #如果被代理服务器返回的状态码为400或者大于400，设置的error_page配置起作用。默认为off。
    proxy_headers_hash_max_size 1024; #存放http报文头的哈希表容量上限，默认为512个字符。
    proxy_headers_hash_bucket_size 128; #nginx服务器申请存放http报文头的哈希表容量大小。默认为64个字符。
    proxy_next_upstream timeout;  #反向代理upstream中设置的服务器组，出现故障时，被代理服务器返回的状态值。error|timeout|invalid_header|http_500|http_502|http_503|http_504|http_404|off
    #proxy_ssl_session_reuse on; 默认为on，如果我们在错误日志中发现“SSL3_GET_FINSHED:digest check failed”的情况时，可以将该指令设置为off。
```
### 5、nginx负载均衡详解
这节详细说明了nginx的操作配置。  
首先说一下upstream这个配置，这个配置是写一组被代理的服务器地址，然后配置负载均衡的算法。这里的被代理服务器的地址有2中写法。  
```
upstream mysvr {
      server 192.168.10.121:3333;
      server 192.168.10.122:3333;
    }
 server {
        ....
        location  ~*^.+$ {         
           proxy_pass  http://mysvr;  #请求转向mysvr 定义的服务器列表         
        }
```
```
upstream mysvr {
      server  http://192.168.10.121:3333;
      server  http://192.168.10.122:3333;
    }
 server {
        ....
        location  ~*^.+$ {         
           proxy_pass  mysvr;  #请求转向mysvr 定义的服务器列表         
        }
```
然后，来点实战的东西。
1、热备：如果你有2台服务器，当一台服务器发生事故时，才启用第二台服务器给提供服务。服务器处理请求的顺序；AAAA突然挂了，BBBB...  
```
upstream mysvr {
      server 127.0.0.1:7878;
      server 192.168.10.121:3333 backup;  #热备     
    }
```
2、轮询：nginx默认就是轮询其权重都默认为1，服务器处理请求的顺序：ABABABAB.....  
```
upstream mysvr {
      server 127.0.0.1:7878;
      server 192.168.10.121:3333;       
    }
```
3、加权轮询：根据配置的权重的大小而分发给不同服务器不同数量的请求。如果不设置，则默认为1。下面服务器的请求顺序为：ABBABBABB.....
```
upstream mysvr {
     server 127.0.0.1:7878 weight=1;
     server 192.168.10.121:3333 weight=2;
}
```
4、ip_hash:nginx会让相同的客户端ip请求相同的服务器。  
```
upstream mysvr {
      server 127.0.0.1:7878;
      server 192.168.10.121:3333;
      ip_hash;
    }
```
5、关于nginx负载均衡配置的几个状态参数讲解
> * down, 表示当前的server暂时不参与负载均衡。
> * backup, 预留的备份机器。当其他所有的非backup机器出现故障或者忙的时候，才会请求backup机器，因此这台机器的压力最轻。
> * max_fails, 允许请求失败的次数，默认为1.当超过最大次数时，返回proxy_next_upstream模块定义的错误。
> * fail_timeout, 在经历了max_fails次失败后，暂停服务的时间。max_fails可以和fail_timeout一起使用.
```
upstream mysvr {
     server 127.0.0.1:7878 weight=2 max_fails=2 fail_timeout=2;
     server 192.168.10.121:3333 weight=1 max_fails=2 fail_timeout=1;    
   }
```
# Nginx Configuration Snippets
A collection of useful Nginx configuration snippets inspired by
[.htaccess snippets](https://github.com/phanan/htaccess).

## Table of Contents
- [The Nginx Command](#the-nginx-command)
- [Rewrite and Redirection](#rewrite-and-redirection)
    - [Force www](#force-www)
    - [Force no-www](#force-no-www)
    - [Force HTTPS](#force-https)
    - [Force Trailing Slash](#force-trailing-slash)
    - [Redirect a Single Page](#redirect-a-single-page)
    - [Redirect an Entire Site](#redirect-an-entire-site)
    - [Redirect an Entire Sub Path](#redirect-an-entire-sub-path)
- [Performance](#performance)
    - [Contents Caching](#contents-caching)
    - [Gzip Compression](#gzip-compression)
    - [Open File Cache](#open-file-cache)
    - [SSL Cache](#ssl-cache)
    - [Upstream Keepalive](#upstream-keepalive)
- [Monitoring](#monitoring)
- [Security](#security)
    - [Enable Basic Authentication](#enable-basic-authentication)
    - [Only Allow Access From Localhost](#only-allow-access-from-localhost)
    - [Secure SSL settings](#secure-ssl-settings)
- [Miscellaneous](#miscellaneous)
    - [Sub-Request Upon Completion](#sub-request-upon-completion)
    - [Enable Cross Origin Resource Sharing](#enable-cross-origin-resource-sharing)
- [Links](#links)

## The Nginx Command
The `nginx` command can be used to perform some useful actions when Nginx is running.

- Get current Nginx version and its configured compiling parameters: `nginx -V`
- Test the current Nginx configuration file and / or check its location: `nginx -t`
- Reload the configuration without restarting Nginx: `nginx -s reload`


## Rewrite and Redirection

### Force www
The [right way](http://nginx.org/en/docs/http/converting_rewrite_rules.html)
is to define a separated server for the naked domain and redirect it.
```nginx
server {
    listen 80;
    server_name example.org;
    return 301 $scheme://www.example.org$request_uri;
}

server {
    listen 80;
    server_name www.example.org;
    ...
}
```

Note that this also works with HTTPS site.

### Force no-www
Again, the right way is to define a separated server for the www domain and redirect it.
```nginx
server {
    listen 80;
    server_name example.org;
}

server {
    listen 80;
    server_name www.example.org;
    return 301 $scheme://example.org$request_uri;
}
```

### Force HTTPS
This is also handled by the 2 server blocks approach.
```nginx
server {
    listen 80;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;

    # let the browsers know that we only accept HTTPS
    add_header Strict-Transport-Security max-age=2592000;

    ...
}
```

### Force Trailing Slash
This configuration only add trailing slash to URL that does not contain a dot because you probably don't want to add that trailing slash to your static files.
[Source](http://stackoverflow.com/questions/645853/add-slash-to-the-end-of-every-url-need-rewrite-rule-for-nginx).
```nginx
rewrite ^([^.]*[^/])$ $1/ permanent;
```

### Redirect a Single Page
```nginx
server {
    location = /oldpage.html {
        return 301 http://example.org/newpage.html;
    }
}
```

### Redirect an Entire Site
```nginx
server {
    server_name old-site.com
    return 301 $scheme://new-site.com$request_uri;
}
```

### Redirect an Entire Sub Path
```nginx
location /old-site {
    rewrite ^/old-site/(.*) http://example.org/new-site/$1 permanent;
}
```


## Performance

### Contents Caching
Allow browsers to cache your static contents for basically forever. Nginx will set both `Expires` and `Cache-Control` header for you.
```nginx
location /static {
    root /data;
    expires max;
}
```

If you want to ask the browsers to **never** cache the response (e.g. for tracking requests), use `-1`.
```nginx
location = /empty.gif {
    empty_gif;
    expires -1;
}
```

### Gzip Compression
```nginx
gzip  on;
gzip_buffers 16 8k;
gzip_comp_level 6;
gzip_http_version 1.1;
gzip_min_length 256;
gzip_proxied any;
gzip_vary on;
gzip_types
    text/xml application/xml application/atom+xml application/rss+xml application/xhtml+xml image/svg+xml
    text/javascript application/javascript application/x-javascript
    text/x-json application/json application/x-web-app-manifest+json
    text/css text/plain text/x-component
    font/opentype application/x-font-ttf application/vnd.ms-fontobject
    image/x-icon;
gzip_disable  "msie6";
```

### Open File Cache
If you have _a lot_ of static files to serve through Nginx then caching of the files' metadata (not the actual files' contents) can save some latency.
```nginx
open_file_cache max=1000 inactive=20s;
open_file_cache_valid 30s;
open_file_cache_min_uses 2;
open_file_cache_errors on;
```

### SSL Cache
Enable SSL cache for SSL sessions resumption, so that sub sequent SSL/TLS connection handshakes can be shortened and reduce total SSL overhead.
```nginx
ssl_session_cache shared:SSL:10m;
ssl_session_timeout 10m;
```

### Upstream Keepalive
Enable the upstream connection cache for better reuse of connections to upstream servers. [Source](http://nginx.org/en/docs/http/ngx_http_upstream_module.html#keepalive).
```nginx
upstream backend {
    server 127.0.0.1:8080;
    keepalive 32;
}

server {
    ...
    location /api/ {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
    }
}
```


## Monitoring

The [Stub Status](http://nginx.org/en/docs/http/ngx_http_stub_status_module.html), which is not built by default, is a very simple to setup module but only provide basic status of Nginx.
```nginx
location /status {
    stub_status on;
    access_log off;
}
```

It provides the following status for the whole Nginx server in plain text(!) format:
- Client connections: accepted, handled, active (includes reading, writing and waiting).
- Total number of client requests.

**[Shameless Plug]** A _better_ way to capture Nginx status can be added by using [Luameter](https://luameter.com) which is a bit more complicated to setup and required the Nginx Lua module (which is awesome). It provides following metrics for each [configurable group](https://luameter.com/configuration) as a JSON API:
- Total number of requests / responses.
- Total number of responses groupped by status code: 1xx, 2xx, 3xx, 4xx, 5xx.
- Total bytes received from / sent to client.
- Sampled latency snapshot for estimation of: mean, max, median, 99th percentile, etc., latency.
- Moving average rate of requests for easier monitoring and predicting.
- And [some more](https://luameter.com/metrics).

[Here is a sample dashboard built with Luameter's metrics](https://luameter.com/demo).

[ngxtop](https://github.com/lebinh/ngxtop) is also a good way to check for Nginx status and checking / troubleshooting a live server.


## Security

### Enable Basic Authentication
You will need a user password file somewhere first.
```
name:{PLAIN}plain-text-password
```

Then add below config to `server`/`location` block that need to be protected.
```nginx
auth_basic "This is Protected";
auth_basic_user_file /path/to/password-file;
```

### Only Allow Access From Localhost
```nginx
location /local {
    allow 127.0.0.1;
    deny all;
    ...
}
```

### Secure SSL settings
- Disable SSLv3 which is enabled by default. This prevents [POODLE SSL Attack](http://nginx.com/blog/nginx-poodle-ssl/).
- Ciphers that best allow protection from Beast. [Mozilla Server Side TLS and Nginx]( https://wiki.mozilla.org/Security/Server_Side_TLS#Nginx)
```nginx
# don’t use SSLv3 ref: POODLE CVE-2014-356 - http://nginx.com/blog/nginx-poodle-ssl/
ssl_protocols  TLSv1 TLSv1.1 TLSv1.2;  

# Ciphers set to best allow protection from Beast, while providing forwarding secrecy, as defined by Mozilla (Intermediate Set) - https://wiki.mozilla.org/Security/Server_Side_TLS#Nginx
    ssl_ciphers 'ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-DSS-AES128-GCM-SHA256:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-DSS-AES128-SHA256:DHE-RSA-AES256-SHA256:DHE-DSS-AES256-SHA:DHE-RSA-AES256-SHA:AES128-GCM-SHA256:AES256-GCM-SHA384:AES128-SHA256:AES256-SHA256:AES128-SHA:AES256-SHA:AES:CAMELLIA:DES-CBC3-SHA:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!MD5:!PSK:!aECDH:!EDH-DSS-DES-CBC3-SHA:!EDH-RSA-DES-CBC3-SHA:!KRB5-DES-CBC3-SHA';
ssl_prefer_server_ciphers  on;

```

## Miscellaneous

### Sub-Request Upon Completion
There are some cases that you want to pass the request to another backend _in addition to and after_ serving it. One use case is to track the number of completed downloads by calling an API after user completed download a file. Another use case is for tracking request where you want to return as fast as possible (perhaps with an `empty_gif`) and then do the actual recording in background. The [post_action](http://wiki.nginx.org/HttpCoreModule#post_action) that allows you to define a sub-request that will be fired upon completion of the current request are [perfect solution](http://mailman.nginx.org/pipermail/nginx/2008-April/004524.html) for these use cases.
```nginx
location = /empty.gif {
    empty_gif;
    expires -1;
    post_action @track; 
}

location @track {
    internal;
    proxy_pass http://tracking-backend;
}
```

### Enable Cross Origin Resource Sharing
Simple, wide-open configuration to allow cross-domain requests to your server.
```nginx
location ~* \.(eot|ttf|woff) {
    add_header Access-Control-Allow-Origin *;
}
```


## Links
Some other awesome resources for configuring Nginx:

- [Nginx Official Guide](http://nginx.com/resources/admin-guide/)
- [HTML 5 Boilerplate's Sample Nginx Configuration](https://github.com/h5bp/server-configs-nginx)
- [Nginx Pitfalls](http://wiki.nginx.org/Pitfalls)
