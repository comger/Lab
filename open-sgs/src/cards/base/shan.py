#!/usr/bin/env python
#coding: utf8

from sgs.cards.cardkind import *
from sgs.utils.uid import getUID
from sgs.triggers.trigger import *

class ShanObj(object):
	"""
		闪卡
	"""
	kind = CK_SHAN
	def __init__(self):
		self.id = getUID()
		self.name = "闪"
		self.desc = "一个字 ”闪“"
	def Apply(self,AO):
		if (AO.card.ObjKind() == CK_SHAN):
			print "凭空闪是没用的..."
		return False
	def Dump(self):
		print "基础技能:",self.name
		print self.desc	
if __name__=="__main__":
	ShanObj().Dump()
