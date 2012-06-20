#!/usr/bin/env python
#coding: utf8

class FakeNet(object):
	def Send(self,msg):
		"""
			发送消息,指令等.
		"""
		print msg
	def Recv(self):
		"""
			得到指令
		"""
		pass
	def Close(self):
		"""
			关闭Socket等操作.
		"""
		try:
			pass
		except:
			pass

class NetManager(object):
	"""
		网络和玩家的管理中心.
	"""
	def __init__(self):
		self.dict = {}  #player: Net
	def add(self,player,net):
		oldnet = self.dict.get(player,None)
		if oldnet: oldnet.Close()
		self.dict[player] = net
	def remove(self,player):
		if player in self.dict:
			self.dict[player].Close() 
			del self.dict[player]
	def get(self,player):  #抛出异常的.
		self.dict.get(player)