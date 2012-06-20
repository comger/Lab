#!/usr/bin/env python
#coding: utf8

from sgs.triggers.trigger import HOOK_ATTACKFAILED
from sgs.cards.cardkind import *
from sgs.cards.arm import Arm
from sgs.players.command import *

class GsfObj(Arm):
	"""
		贯石斧
	"""
	kind = CK_GSF
	def __init__(self):
		Arm.__init__(self,"贯石斧","斧，甫也，甫，始也.凡将制器，始用斧伐木，已乃制之也 -- 释名.释用器")
	def Apply(self,player,db):
		self.db = db
		self.db.Hook(HOOK_ATTACKFAILED,self)
	def unApply(self):
		if not self.db: return
		#--从player中去除掉这个装备--
		self.db.unHook(HOOK_ATTACKFAILED,self)
	def HOOK_ATTACKFAILED(self,AO):
		if AO.card.ObjKind() != CK_SHA: return False
		me = AO.src
		cmd = me.getCmd()
		if cmd.kind != CMD_DROP:
			me.pushCmd(cmd)
			return False
		if len(cmd.poslist) != 2:
			me.pushCmd(cmd)
			return False
		AO.src.Qi(cmd.poslist)
		AO.target.Damage(me.damage)
		AO.target.Notify(HOOK_HURTED,AO,me.damage) #通知这个玩家，你受到伤害了,而且还是受到了damage的伤害.
		return True
if __name__=="__main__":
	pass
