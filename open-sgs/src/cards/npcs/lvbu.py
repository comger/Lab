#!/usr/bin/env python
#coding: utf8


from sgs.cards.npc import NPC,MALE
from sgs.cards.cardkind import *
from sgs.triggers.trigger import HOOK_ATTACK
from sgs.aos.ao import AOReq_AND,AOReqItem,AOReq_OR
 
class LvBu(NPC):
	def __init__(self):
		NPC.__init__(self, "吕布",4,MALE,"骁勇无敌，善战无前，然勇而无谋，暴而少仁！")
	def Apply(self,db):
		db.Hook(HOOK_ATTACK,self)
		db.Hook(HOOK_SPELL,self)
	def HOOK_ATTACK(self,AO):
		if AO.card and AO.card.ObjKind() == CK_SHA: #使用的是杀,修改现在采用AOReq_AND.
			req = AOReq_AND()
			req.Append(AOReqItem(CK_SHAN))
			req.Append(AOReqItem(CK_SHAN))
			AO.req = req
	def HOOK_SPELL(self,AO):
		if AO.card and AO.card.ObjKind() == CK_JUEDOU: #决斗.
			ret = AOReq_OR()
			req = AOReq_AND()
			req.Append(AOReqItem(CK_SHA))
			req.Append(AOReqItem(CK_SHA))
			ret.Append(req)
			ret.Append(AOReqItem(CK_WXKJ))
			AO.req = ret
if __name__=="__main__":
	LvBu().Dump()
