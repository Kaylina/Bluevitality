#!/usr/bin/env python

import argparse
parser = argparse.ArgumentParser( prog='usage_name', description='开头打印', epilog="结束打印")

parser.add_argument('-f', '--foo', help='foo help', action='append')      
# 可选参数,如使用此参数必须传值 action='store_true' 不加参数为True  action='append' 多个参数可叠加为列表

parser.add_argument('--aa', type=int, default=42, help='aa!')             # type规定参数类型,default设置默认值
parser.add_argument('bar', nargs='*', default=[1, 2, 3], help='BAR!')     # 位置参数 必须传递  nargs=2 需要传递2个参数
parser.add_argument('args', nargs=argparse.REMAINDER)                     # 剩余参数收集到列表
parser.print_help()                                                       # 打印使用帮助
#parser.parse_args('BAR --foo FOO'.split())                               # 设置位置参数
args = parser.parse_args()                                                # 全部的值
parser.get_default('foo')                                                 # 获取

python a.py --foo ww  --aa 40 xuesong 27                                  # 执行此脚本
