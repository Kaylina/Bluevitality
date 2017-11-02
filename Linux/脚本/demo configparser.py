#!/usr/bin/env python

#写入配置文件
import ConfigParser
config = ConfigParser.RawConfigParser()
config.add_section('Section1')                          # 添加配置文件的块 [name]
config.set('Section1', 'an_int', '15')                  # 针对块设置配置参数和值
config.set('Section1', 'a_bool', 'true')
config.set('Section1', 'a_float', '3.1415')
config.set('Section1', 'baz', 'fun')
config.set('Section1', 'bar', 'Python')
config.set('Section1', 'foo', '%(bar)s is %(baz)s!')
with open('example.cfg', 'wb') as configfile:           # 指定配置文件路径
    config.write(configfile)                            # 写入配置文件

#读取配置文件
import ConfigParser
config = ConfigParser.RawConfigParser()
config.read('example.cfg')                              # 读取配置文件
a_float = config.getfloat('Section1', 'a_float')        # 获取配置文件参数对应的浮点值,如参数值类型不对则报ValueError
an_int = config.getint('Section1', 'an_int')            # 获取配置文件参数对应的整数值,可直接进行计算
print a_float + an_int
if config.getboolean('Section1', 'a_bool'):             # 根据配置文件参数值是否为真
    print config.get('Section1', 'foo')                 # 再获取依赖的配置参数 get获取后值为字符串
print config.get('Section1', 'foo', 0)                  # 获取配置文件参数的同时加载变量[配置文件中的参数]
print config.get('Section1', 'foo', 1)                  # 获取配置文件参数 原始值不做任何改动 不使用变量
config.remove_option('Section1', 'bar')                 # 删除读取配置文件获取bar的值
config.remove_option('Section1', 'baz')
print config.get('Section1', 'foo', 0, {'bar': 'str1', 'baz': 'str1'})    # 读取配置参数的同时设置变量的值


#demo
import ConfigParser
import io

sample_config = """
[mysqld]
user = mysql
pid-file = /var/run/mysqld/mysqld.pid
skip-external-locking
old_passwords = 1
skip-bdb
skip-innodb
"""
config = ConfigParser.RawConfigParser(allow_no_value=True)
config.readfp(io.BytesIO(sample_config))
config.get("mysqld", "user")
