#!/usr/bin/env python
#coding: utf8

from sgs.cards.cardkind import *
from sgs.cards.arm import Arm

class JyObj(Arm):
	"""
		绝影
	"""
	kind = CK_JY
	def __init__(self):
		Arm.__init__(self,"绝影","公所乘马名绝影 <三国志.魏书>")
	def Apply(self,player,db):
		self.player = player
		self.player.attack_range += 1
	def unApply(self):
		if self.player.attack_range > 0:
			self.player.attack_range -= 1
if __name__=="__main__":
	pass
