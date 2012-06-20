#!/usr/bin/env python
#coding: utf8

from sgs.cards.cardkind import CK_WXKJ
from sgs.cards.spell import Spell
from sgs.triggers.trigger import *

class WxkjObj(Spell):
	"""
		无懈可击
	"""	
	kind = CK_WXKJ
	def __init__(self):
		Spell.__init__(self, "无懈可击", "击其懈怠，出其空虚--曹操")
	def Apply(self,AO):
		"""
		"""
		print "又没人法术你，慌什么？"
if __name__=="__main__":
	print WxkjObj.kind
	print WxkjObj().getReq()
