#!/usr/bin/env python
#coding: utf8

from sgs.cards.cardkind import CK_NMRQ,CK_WXKJ,CK_SHA
from sgs.cards.spell import Spell
from sgs.triggers.trigger import *
import sgs.players.answer
from sgs.aos.ao import AOReqItem,AOReq_OR
from sgs.resource.vars import GameVar

class NmrqObj(Spell):
	"""
		南蛮入侵
	"""	
	kind = CK_NMRQ
	def __init__(self):
		Spell.__init__(self, "南蛮入侵", "南蛮一人持矛入侵，川兵百人见而奔逃 --无名氏")
	def getReq(self):
		ao = AOReq_OR()
		ao.Append(AOReqItem(CK_WXKJ)) #需要无懈可击
		ao.Append(AOReqItem(CK_SHA)) #需要杀
		return ao
	def Apply(self,AO):
		i = AO.src.findCard(AO.card)
		if i < 0: raise Exception("卡不见了")
		AO.src.Qi([i])  #丢掉这张牌了.
		
		AO.src.Notify(HOOK_SPELL,AO)           #首先通知自身，我出法术攻击牌了.
		targets = GameVar.getOtherPlayer(AO.src)
		req = AO.req
		for target in targets:
			AO.target = target
			AO.req = req.Clone()
			target.Notify(HOOK_ATTACKED,AO)       #通知对象，被攻击了.
			target.Notify(HOOK_SPELLED,AO)      #通知对象，被攻击了.
			if sgs.players.answer.Answer(AO):       #等待应答.
#				AO.src.Notify(HOOK_SPELLFAILED,AO) #法术攻击失败了.
				continue
			target.Damage(1)
			target.Notify(HOOK_HURTED,AO,1) #通知这个玩家，你受到伤害了,而且还是受到了damage的伤害.
if __name__=="__main__":
	pass
