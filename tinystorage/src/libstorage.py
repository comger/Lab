#!/usr/bin/env python2
#coding: utf8
import socket,select,struct
import sys,zlib
from message import *

try:
	import cStringIO as StringIO
except:
	import StringIO

class KVClient(object):
	@classmethod
	def getClient(self,addrstr):
		m = addrstr.split(":")	
		if len(m) != 2:
			raise Exception("Client Addr[%s] Format Failed" % addrstr)
		return KVClient((m[0],int(m[1])))
	def __init__(self,addr):
		"""
			addr: 服务端的地址(HOST,PORT)
		"""
		self.rfile = None
		self.wfile = None
		host,port = addr
		if host[0]=='[' and host[-1] == ']':
			self.sock=socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
			host = host[1:-1]
		else:
			self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.connect( (host,port) )
		self.sock.settimeout(60)
		self.rfile=self.sock.makefile("r",4096)
		self.wfile=self.sock.makefile('w',4096)
	def __del__(self):
		self.close()
	def close(self):
		def close_i(obj):
			try:
				obj.close()
			except:
				pass
		if self.rfile:
			close_i(self.rfile)
		if self.wfile:
			close_i(self.wfile)
		if self.sock:
			close_i(self.sock)
		self.rfile = None
		self.wfile = None
		self.sock  = None

	def delete(self,key): #删除一个
		if not self.wfile or not self.rfile: raise Exception("Client Closed")
		deleteMsg(key).socketsend(self.wfile)

	def write(self,key,data):#写入一个
		if not self.wfile or not self.rfile: raise Exception("Client Closed")
		writeMsg(key,data).socketsend(self.wfile)	

	def read(self,key):
		if not self.wfile or not self.rfile: raise Exception("Client Closed")
		readMsg(key).socketsend(self.wfile)	 #发送请求
		msg = getsocketMessage(self.rfile)
		if msg['key'] != key:
			raise Exception("Read Failed ret Key[%s] !=key[%s]" % (msg['key'],key))
		return msg.data

def test():
	from basetools import now
	client = KVClient.getClient("localhost:5555")
	data = '*'*1024
	a = now()
	for x in xrange(100000):
		client.write("heihei%s"%x,data+'%s'%x)
	b=now()
	print "---->",b-a,"sss"
	print client.read("heihei90000")
if __name__=="__main__":
	test()

