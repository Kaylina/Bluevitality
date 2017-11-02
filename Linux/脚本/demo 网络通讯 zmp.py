#!/usr/bin/env python
# need pip install pyzmq

#服务端程序
import zmq
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://127.0.0.1:1234")         # 提供传输协议  INPROC  IPC  MULTICAST  TCP

while True :
    msg = socket.recv()
    socket.send(msg)

#客户端端程序
import zmq
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:1234")
# socket.connect("tcp://127.0.0.1:6000")    # 设置2个可以均衡负载请求到2个监听的server
msg_send = "xxx"
socket.send(msg_send)
print "Send:", msg_send
msg_recv = socket.recv()
print "Receive:", msg_recv
