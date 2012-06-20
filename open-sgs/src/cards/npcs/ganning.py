#!/usr/bin/env python
#coding: utf8

from sgs.cards.npc import NPC,MALE
from sgs.cards.cardkind import *
from sgs.cards.card import Card,MEIHUA,HEITAO
from sgs.cards.spells.ghcq import GhcqObj
from sgs.triggers.trigger import HOOK_SKILL
from sgs.aos.ao import AOReqItem

class GanNing(NPC):
	def __init__(self):
		NPC.__init__(self, "甘宁",4,MALE,"孟德有张辽，孤有甘兴霸，足可敌敌矣！")
	def Apply(self,db):
		db.Hook(HOOK_SKILL,self)
	def HOOK_SKILL(self,ao):
		"""
			当HOOK_SKILL被激活时.
			也就是使用特殊技能的时候.
		"""
		if ao.card and ao.card.kind not in [HEITAO,MEIHUA]: return False		
		ao.card = Card(0,0,GhcqObj())
		ao.req = ao.card.obj.getReq()
		ao.src.addCard(ao.card) #加入这张牌，以便马上被用掉
		return True
if __name__=="__main__":
	#GanNing().Dump()
	v = "HOOK_SKILL"
	g = GanNing()
