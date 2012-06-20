#!/usr/bin/env python
#coding: utf8

from sgs.cards.cardkind import CK_TYJY
from sgs.cards.spell import Spell
from sgs.triggers.trigger import *
from sgs.resource.vars import GameVar

class TyjyObj(Spell):
	"""
		桃园结义
	"""	
	kind = CK_TYJY
	def __init__(self):
		Spell.__init__(self, "桃园结义", "既结为兄弟，则同心协力，救困扶危；上报国家，下安黎庶。不求同年同月同日生，只愿同年同月同日死。皇天后土，实鉴此心，背义忘恩，天人共戮 ---三国演义")
	def Apply(self,AO):
		"""
			主动用的
		"""
		i = AO.src.findCard(AO.card)
		if i < 0: raise Exception("卡不见了")
		AO.src.Qi([i])  #丢掉这张牌了.
		
		for player in GameVar.getLivingPlayer():
			player.Heal(1)  #如果有加倍治疗的，请在HOOK_HEALED中处理.
			player.Notify(HOOK_HEALED,AO)
if __name__=="__main__":
	pass
