#!/usr/bin/env python
#coding: utf8

from sgs.cards.cardkind import CK_Sd,CK_WXKJ
from sgs.cards.spell import Spell
from sgs.cards.card import HEITAO
from sgs.triggers.trigger import *
from sgs.resource.vars import GameVar
import sgs.players.answer
import sgs.utils

class SdObj(Spell):
	"""
		闪电
	"""	
	kind = CK_LBSS
	def __init__(self):
		Spell.__init__(self, "闪电", "啊啊啊，电死人又不偿命的咯!")
	def PangDing(self,player,card):
		print "闪电盘旋，请选择如何应对"
		if sgs.players.answer.Answer(AO):   #等待应答.
			GameVar.nextplayer().addWaiting(card)
			return
		cardlist = sgs.utils.cardop.getHeadCard(1)
		card = cardlist[0]
		print "判定牌是:",card
		GameVar.NotifyAll(HOOK_PANGDING,card) #需要通知全部人了，因为司马懿是可以篡改自己的
		#-----------------------------------------------------
		if (2 <= card.point <=9) and (card.kind == HEITAO):
			player.Damage(3)
			return
		GameVar.nextplayer().addWaiting(card)
	def Apply(self,AO):
		i = AO.src.findCard(AO.card)
		if i < 0: raise Exception("卡不见了")
		AO.src.Qi([i])  #丢掉这张牌了.
		AO.src.addWaiting(AO.card)
if __name__=="__main__":
	pass
