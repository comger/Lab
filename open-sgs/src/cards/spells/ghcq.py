#!/usr/bin/env python
#coding: utf8

from sgs.cards.cardkind import CK_GHCQ
from sgs.cards.spell import Spell
from sgs.triggers.trigger import *
from sgs.players.command import CMD_SELECT
import sgs.players.answer

class GhcqObj(Spell):
	"""
		过河拆桥
	"""	
	kind = CK_GHCQ
	def __init__(self):
		Spell.__init__(self, "过河拆桥", "你休的顺水推舟，偏不许我过河拆桥－－康进之")
	def Apply(self,AO):
		"""
			主动用的.
		"""
		i = AO.src.findCard(AO.card)
		if i < 0: raise Exception("卡不见了")
		AO.src.Qi([i])  #丢掉这张牌了.
		
		AO.src.Notify(HOOK_SPELL,AO)           #首先通知自身，我出法术攻击牌了.
		AO.target.Notify(HOOK_SPELLED,AO)      #通知对象，被攻击了.
		if sgs.players.answer.Answer(AO):          #等待应答.
			AO.src.Notify(HOOK_SPELLFAILED,AO) #法术攻击失败了.
			return
		AO.target.HP() #显示下被法术攻击者还有什么东东.
		cmd = AO.src.getCmd()
		while cmd.kind != CMD_SELECT:
			print "请选择要拆掉的牌"
			cmd = AO.src.getCmd()
		card = AO.target.lookCard(cmd.poslist)
		AO.target.Qi(cmd.poslist)
		AO.target.Notify(HOOK_LOST,card) #通知这个玩家，丢失一张牌.
if __name__=="__main__":
	print GHCQ.kind
	print GHCQ().getReq()
	print GHCQ().getReq()
	print GHCQ().id
	GHCQ().Dump()
