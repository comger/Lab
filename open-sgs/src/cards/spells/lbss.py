#!/usr/bin/env python
#coding: utf8

from sgs.cards.cardkind import CK_LBSS
from sgs.cards.spell import Spell
from sgs.cards.card import HONGTAO,FANGKUAI
from sgs.triggers.trigger import *
from sgs.resource.vars import GameVar
import sgs.players.answer
import sgs.utils

class LbssObj(Spell):
	"""
		乐不思蜀
	"""	
	kind = CK_LBSS
	def __init__(self):
		Spell.__init__(self, "乐不思蜀", "问禅曰：'颇思蜀否？'禅曰：'此间乐，不思蜀。")
	def PangDing(self,player,card):
		"""
			先从waiting中取走这张牌.
		"""
		cardlist = sgs.utils.cardop.getHeadCard(1)
		card = cardlist[0]
		print "判定牌是:",card
		GameVar.NotifyAll(HOOK_PANGDING,card) #需要通知全部人了，因为司马懿是可以篡改自己的
		#-----------------------------------------
		if card.kind in [HONGTAO,FANGKUAI]: return
		player.StopChuPai()		
	def Apply(self,AO):
		i = AO.src.findCard(AO.card)
		if i < 0: raise Exception("卡不见了")
		AO.src.Qi([i])  #丢掉这张牌了.
		
		AO.src.Notify(HOOK_SPELL,AO)      #首先通知自身，我出法术攻击牌了.
		if sgs.players.answer.Answer(AO):     #等待应答.
			return
		AO.target.addWaiting(AO.card)
if __name__=="__main__":
	pass
