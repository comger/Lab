#!/usr/bin/env python
#coding: utf8

from sgs.cards.cardkind import CK_WZSY
from sgs.cards.spell import Spell
from sgs.triggers.trigger import *

class WzsyObj(Spell):
	"""
		无中生有
	"""	
	kind = CK_WZSY
	def __init__(self):
		Spell.__init__(self, "无中生有", "天下万物生于有，有生于无 --老子")
	def Apply(self,AO):
		"""
			摸两张牌
		"""
		i = AO.src.findCard(AO.card)
		if i < 0: raise Exception("卡不见了")
		AO.src.Qi([i])  #丢掉这张牌了.
		
		AO.src.getExtraCard(2)
if __name__=="__main__":
	print GHCQ.kind
	print GHCQ().getReq()
	print GHCQ().getReq()
	print GHCQ().id
	GHCQ().Dump()
