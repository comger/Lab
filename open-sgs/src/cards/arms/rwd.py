#!/usr/bin/env python
#coding: utf8

from sgs.triggers.trigger import HOOK_ATTACKED
from sgs.cards.cardkind import *
from sgs.cards.arm import Arm
from sgs.cards.card import HEITAO,MEIHUA

class RwdObj(Arm):
	kind = CK_RWD
	def __init__(self):
		Arm.__init__(self,"仁王盾","")
	def Apply(self,player,db):
		self.db = db
		self.db.Hook(HOOK_ATTACKED,self)
	def unApply(self):
		if not self.db: return
		#--从player中去除掉这个装备--
		self.db.unHook(HOOK_ATTACKED,self)
	def HOOK_ATTACKED(self,AO):
		if AO.Answered(): return   #已经匹配成功的了.
		if (AO.card.ObjKind() == CK_SHA) and (AO.card.kind in [HEITAO,MEIHUA]):
			AO.req = None
if __name__=="__main__":
	pass
