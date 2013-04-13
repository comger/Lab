#coding: utf8
#消息发送来回通过marshal发送
#消息格式为:
#[int] -> 4字节,消息长度
#[marshaledcontent] -> 的内容.
#ok: true/false -> 是否成功

import marshal,struct

class Msg(object):
	def __init__(self):
		self._val = {'ok':True}
	def iscmd(self):
		return 'cmd' in self._val
	def isok(self):
		return self._val['ok']
	def __setitem__(self,key,value):
		key = '%s' % key
		self._val[key] = value
	def __getitem__(self,key):
		key = '%s' % key
		if key in self._val: return self._val[key]
		return None
	def __contains__(self,key):
		key = '%s' % key
		return key in self._val
	def pack(self):
		return marshal.dumps(self._val)
	@staticmethod
	def unpack(content):
		msg = Msg()
		msg._val = marshal.loads(content)
		return msg
	def send(self,stream,cb=None):
		v = self.pack() #Head头部
		if cb:
			stream.write('%s%s' % (struct.pack('I',len(v)),v),cb)
		else:
			stream.write('%s%s' % (struct.pack('I',len(v)),v))
	def socketsend(self,sock):
		v = self.pack() #Head头部
		sock.write('%s%s' % (struct.pack('I',len(v)),v))
		sock.flush()

class errMsg(Msg):
	"""错误消息"""
	def __init__(self,errmsg):
		super(errMsg,self).__init__()
		self['ok'] = False
		self['errmsg'] = errmsg

class cmdMsg(Msg):
	"""命令消息"""
	def __init__(self,cmd):
		super(cmdMsg,self).__init__()
		self['cmd'] = cmd
		
class readMsg(cmdMsg):
	"""读取消息"""
	def __init__(self,key):
		super(readMsg,self).__init__('read')
		self['key'] =key 

class writeMsg(cmdMsg):
	"""写入消息"""
	def __init__(self,key,data):
		super(writeMsg,self).__init__('write')
		self['key'] = key 
		self['size'] = len(data)
		self.data = data #引用这批数据(为了避免多次Copy可以用memoryview)
	def send(self,stream,cb=None):
		v = self.pack() #Head头部
		head = '%s%s' % (struct.pack('I',len(v)),v)
		stream.write(head)
		if cb:
			stream.write(self.data,cb)
		else:
			stream.write(self.data)
	def socketsend(self,sock):
		v = self.pack() #Head头部
		head = '%s%s' % (struct.pack('I',len(v)),v)
		sock.write(head)
		sock.write(self.data)
		sock.flush()

class deleteMsg(cmdMsg):
	"""删除消息"""
	def __init__(self,key):
		super(deleteMsg,self).__init__('delete')
		self['key'] = key

def getsocketMessage(sock):
	"""
		从socket中获取数据.
	"""
	ll, = struct.unpack('I',sock.read(4))
	data = sock.read(ll)
	msg = Msg.unpack(data)	
	if msg['cmd'] == 'write': #写入指令
		msg.data = sock.read(msg['size'])
	return msg

import functools
def getMessage(stream,cb):
	"""
		如果size太大，那么需要慢慢的获取数据的了.
		最大超过Tornado的限制，会永远的接受不到，潜在的风险。
	"""
	def getcontent(cb,msg,data):
		msg.data = data
		cb(msg)

	def getdata(data):
		msg = Msg.unpack(data)	
		if msg['cmd'] == 'write': #写入指令
			cpb = functools.partial(getcontent,cb,msg)
			stream.read_bytes(msg['size'],cpb)
		else:
			cb(msg)

	def getsize(ss):
		size, = struct.unpack('I',ss)	
		stream.read_bytes(size,getdata)

	stream.read_bytes(4,getsize)
