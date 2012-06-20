#!/usr/bin/env python
#coding: utf8

from sgs.triggers.trigger import HOOK_ATTACKOK,HOOK_ATTACK,HOOK_ATTACKFAILED,HOOK_ATTACKED
from sgs.cards.cardkind import *
from sgs.cards.arm import Arm
from sgs.players.command import *
class QgjObj(Arm):
	"""
		青釭剑
	"""
	kind = CK_QGJ
	def __init__(self):
		Arm.__init__(self,"青釭剑")
	def Apply(self,player,db):
		self.db = db
		self.db.Hook(HOOK_ATTACK,self)
		self.db.Hook(HOOK_ATTACKFAILED,self)
		self.db.Hook(HOOK_ATTACKOK,self)
	def unApply(self):
		if not self.db: return
		#--从player中去除掉这个装备--
		self.db.unHook(HOOK_ATTACK,self)
		self.db.unHook(HOOK_ATTACKFAILED,self)
		self.db.unHook(HOOK_ATTACKOK,self)
	def HOOK_ATTACKOK(self,AO):
		if AO.card.ObjKind() != CK_SHA: return False
		AO.target.EnableHook(HOOK_ATTACKED)
		return False
	def HOOK_ATTACKFAILED(self,AO):
		if AO.card.ObjKind() != CK_SHA: return False
		AO.target.EnableHook(HOOK_ATTACKED)
		return False
	def HOOK_ATTACK(self,AO):
		if AO.card.ObjKind() != CK_SHA: return False
		AO.target.DisableHook(HOOK_ATTACKED)
		return True
if __name__=="__main__":
	pass
