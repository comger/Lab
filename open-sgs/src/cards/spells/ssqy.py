#!/usr/bin/env python
#coding: utf8

from sgs.cards.cardkind import CK_SSQY
from sgs.cards.spell import Spell
from sgs.triggers.trigger import *
from sgs.players.command import CMD_SELECT
import sgs.players.answer

class SsqyObj(Spell):
	"""
		顺手牵羊
	"""	
	kind = CK_SSQY
	def __init__(self):
		Spell.__init__(self, "顺手牵羊", "效马效羊者右牵之--礼记.曲礼上")
	def Apply(self,AO):
		"""
			主动用的
		"""
		i = AO.src.findCard(AO.card)
		if i < 0: raise Exception("卡不见了")
		AO.src.Qi([i])  #丢掉这张牌了.
		
		AO.src.Notify(HOOK_SPELL,AO)           #首先通知自身，我出法术攻击牌了.
		AO.target.Notify(HOOK_SPELLED,AO)      #通知对象，被攻击了.
		if sgs.players.answer.Answer(AO):          #等待应答.
			AO.src.Notify(HOOK_SPELLFAILED,AO) #法术攻击失败了.
			return
		cmd = AO.src.getCmd()
		while (cmd.kind != CMD_SELECT) or (len(cmd.poslist) != 1):
			print "请选择要拿走的牌"
			cmd = AO.src.getCmd()		
		card = AO.target.lookCard(cmd.poslist)
		AO.target.Qi(cmd.poslist)
		AO.src.addCard(card[0])     #得到一张牌了
		AO.target.Notify(HOOK_LOST,card) #通知这个玩家，丢失一张牌.
if __name__=="__main__":
	pass
