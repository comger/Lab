#!/usr/bin/env python


		
class PlayerMsg(object):
	"""
		消息.
	"""
	def __init__(self,player):
		self.player = player
	def info(self,msg):
		"""
			给自己发消息的.
		"""
		self.net.Send(msg)
	def tell(self,otherplayer,msg):
		"""
			告诉某人某个消息
		"""
#		net = .Send(msg)
	def boardcast(self,msg):
		"""
			广播消息.
		"""
		pass