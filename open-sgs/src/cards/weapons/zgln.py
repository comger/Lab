#!/usr/bin/env python
#coding: utf8

from sgs.triggers.trigger import HOOK_ATTACK
from sgs.cards.cardkind import *
from sgs.cards.arm import Arm

class ZglnObj(Arm):
	"""
		诸葛连弩
	"""
	kind = CK_ZGLN
	def __init__(self):
		Arm.__init__(self,"诸葛连弩","又名损益连驽，谓之元戎，以铁为矢，矢长八寸，一驽十矢俱发  ---<魏氏春秋>")
	def Apply(self,player,db):
		self.db = db
		self.db.Hook(HOOK_ATTACK,self)
	def unApply(self):
		if not self.db: return
		self.db.unHook(HOOK_ATTACK,self)
	def HOOK_ATTACK(self,AO):
		AO.src.usekill = 1  #又可以杀一次的了.		
if __name__=="__main__":
	pass
