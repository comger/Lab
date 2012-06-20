#!/usr/bin/env python
#coding: utf8

from sgs.triggers.trigger import HOOK_ATTACKFAILED
from sgs.cards.cardkind import *
from sgs.cards.arm import Arm
from sgs.players.command import *
from sgs.resource.vars import GameVar

class QlyydObj(Arm):
	"""
		青龙偃月刀
	"""
	kind = CK_QLYYD
	def __init__(self):
		Arm.__init__(self,"青龙偃月刀","刀势即大，其三十六刀法，兵仗遇之，无不屈者，刀类中以此为第一")
	def Apply(self,player,db):
		"""
			安装需要出杀失败的时候钩子.
		"""
		self.db = db
		self.player = player
		self.db.Hook(HOOK_ATTACKFAILED,self)
	def unApply(self):
		if not self.db: return
		#--从player中去除掉这个装备--
		self.db.unHook(HOOK_ATTACKFAILED,self)
	def HOOK_ATTACKFAILED(self,AO):
		me = AO.src
		me.HP()
		cmd = me.getCmd()
		if cmd.kind != CMD_USE:   return me.pushCmd(cmd)
		if len(cmd.poslist) != 1: return me.pushCmd(cmd)
		card, = me.lookCard(cmd.poslist)
		
		if card.ObjKind() != CK_SHA: return me.pushCmd(cmd)
		if AO.target != cmd.target:  return me.pushCmd(cmd)
		me.Qi(cmd.poslist)  #启掉这张牌.
		AO.card = card
		card.Apply(AO)
		
if __name__=="__main__":
#	BgzObj().Dump()
	b = QlyydObj()
	method = getattr(b,'HOOK_ATTACKED')
	print method
