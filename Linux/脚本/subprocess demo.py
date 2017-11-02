#!/usr/bin/env python

import subprocess
s=subprocess.Popen('ls', shell=True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
print s.stdout.read()
print s.stderr.read()
print s.wait()         # 等待子进程结束。并返回执行状态 shell 0为正确
