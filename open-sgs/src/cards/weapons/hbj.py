#!/usr/bin/env python
#coding: utf8

from sgs.triggers.trigger import HOOK_ATTACKOK
from sgs.cards.cardkind import *
from sgs.cards.arm import Arm
from sgs.players.command import *

class HbjObj(Arm):
	"""
		寒冰剑
	"""
	kind = CK_HBJ
	def __init__(self):
		Arm.__init__(self,"寒冰剑")
	def Apply(self,player,db):
		self.db = db
		self.db.Hook(HOOK_ATTACKOK,self)
	def unApply(self):
		if not self.db: return
		#--从player中去除掉这个装备--
		self.db.unHook(HOOK_ATTACKOK,self)
	def HOOK_ATTACKOK(self,AO):
		if AO.card.ObjKind() != CK_SHA: return False
		AO.target.HP()
		print "%s选择弃掉%s最多2张牌而不造成伤害么?放弃直接用F,选择用S" % (AO.src.name,AO.target.name)
		me = AO.src
		cmd = me.getCmd()
		while (cmd.kind not in [CMD_SELECT,CMD_FIN]) or (cmd.kind == CMD_SELECT and (len(cmd.poslist) not in [1,2])):
			print "%s选牌错误"
			cmd = me.getCmd()
		if cmd.kind == CMD_FIN: return False
		AO.target.Qi(cmd.poslist)  #启掉这张牌,不一定是手牌的.
		return True
if __name__=="__main__":
	pass
