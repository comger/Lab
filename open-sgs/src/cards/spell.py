#!/usr/bin/env python
#coding: utf8

from sgs.utils.uid import getUID
from sgs.aos.ao import AOReqItem

from cardkind import *

class Spell(object):
	kind = CK_SPELL
	def __init__(self,name,desc=""):
		self.name = name
		self.desc = desc
		self.id   = getUID()
		
	def getReq(self):
		"""
			应答这个卡需要的对策
		"""
		return AOReqItem(CK_WXKJ) #需要无懈可击
	
	def Apply(self,AO):
		"""
			成功使用该法术.
		"""
		pass
	def Dump(self):
		print "锦囊:",self.name
		if self.desc: print self.desc
	
