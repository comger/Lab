#!/usr/bin/env python2
#coding: utf8

import functools,errno,socket

from tornado import iostream
from tornado import ioloop
from message import *

from storage import textStorage
from indexer import sqliteIndexer,leveldbIndexer

indexerobj = None
storageobj = None

class Runner(object):
	runners = set() #正在运行的
	def __init__(self,conn):
		conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
		self._stream = iostream.IOStream(conn)
		self._stream.set_close_callback(self._close)
		self.__class__.runners.add(self)

		self._handle()
	def _handle(self):
		getMessage(self._stream,self._parse_cmd)
	def _close(self):
		try:
			self.__class__.runners.remove(self)
		except Exception,msg:
			print "@Runner.close",msg
	def _closestream(self): self._stream.close()
	def _handle_delete(self,msg):
		global storageobj,indexerobj

		key = msg['key']
		storageobj.delete(key)
		indexerobj.delete(key)

		self._handle()
	def _handle_write(self,msg):
		global storageobj,indexerobj

		key = msg['key']
		data = msg.data #这个是data，而不是['data']

		offset = storageobj.write(key,data)
		indexerobj.write(key,offset)

		self._handle()
	def _handle_read(self,msg):
		global storageobj,indexerobj

		key = msg['key']
		offset = indexerobj.read(key)

		if offset < 0: #没有的
			writeMsg(key,'').send(self._stream)
		else:
			writeMsg(key,storageobj.read(key,offset)).send(self._stream)
		self._handle()
	def _parse_cmd(self,msg):
		if not msg.iscmd():
			return self._closestream()

		cmd = msg['cmd'].lower()
		route = {
			'read' : self._handle_read,
			'write' : self._handle_write,
			'delete' : self._handle_delete,
		}
		route.get(cmd,self._handle_unknown)(msg)
	def _handle_unknown(self,nouse):
		errMsg("unknown cmd").send(self._stream,self._closestream)

def runServer(addr,indexfile,datafile):
	"""
		addr: (host,addr)
		datadir: 持久化存储的任务文件所在目录.
	"""
	def handle_accept(sock,fd, events):
		try:
			conn, address = sock.accept()
		except socket.error, e:
			if e.args[0] not in (errno.EWOULDBLOCK, errno.EAGAIN):
				raise
			return
		Runner(conn)

	host,port = addr	
	if host[0] == '[' and host[-1] == ']': #IPV6地址.
   		sock = socket.socket(socket.AF_INET6,socket.SOCK_STREAM)
		host = host[1:-1]
	else:
  	 	sock= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.setblocking(0)
	sock.bind((host,port))
	sock.listen(128)

	print "Binding @",host,port
	#-------------------------------------
	global 	indexerobj,storageobj
#	indexerobj = sqliteIndexer(indexfile)
	indexerobj = leveldbIndexer(indexfile)
	storageobj = textStorage(datafile)
	storageobj.start()
	#-------------------------------------
	io_loop = ioloop.IOLoop.instance()
	callback = functools.partial(handle_accept,sock)
	io_loop.add_handler(sock.fileno(), callback, io_loop.READ)

	io_loop.start()

if __name__=="__main__":
	import sys
	if len(sys.argv) != 3:
		print "Usage:",sys.argv[0]," IndexFile DataFile"
		sys.exit(0)
	runServer( ("localhost",5555),sys.argv[1],sys.argv[2])
