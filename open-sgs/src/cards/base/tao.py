#!/usr/bin/env python
#coding: utf8

from sgs.cards.cardkind import *
from sgs.utils.uid import getUID

class TaoObj(object):
	"""
		桃
	"""
	kind = CK_TAO
	def __init__(self,name="桃",heal=1,desc="救命必备,桃之夭夭"):
		self.id = getUID()
		self.name = name
		self.desc = desc
		self.heal = heal   #默认桃的疗效是1，以后会有仙桃的.	
	def Apply(self,AO):
		AO.target.Heal(self.heal)
	def Dump(self):
		print "基础技能:",self.name
		print self.desc	
if __name__=="__main__":
	TaoObj().Dump()
