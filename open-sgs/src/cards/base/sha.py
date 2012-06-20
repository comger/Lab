#!/usr/bin/env python
#coding: utf8

from sgs.cards.cardkind import *
from sgs.utils.uid import getUID
from sgs.aos.ao import AOReqItem
from sgs.triggers.trigger import *
import sgs.players.answer

class ShaObj(object):
	"""
		杀卡
	"""
	kind = CK_SHA
	def __init__(self):
		self.id = getUID()
		self.name = "杀"
		self.desc = "一个字 ”杀“"
	def getReq(self):
		"""
			杀卡对应的对策
		"""
		return AOReqItem(CK_SHAN) #需要一个闪的.
	
	def Apply(self,AO):
		AO.src.Notify(HOOK_ATTACK,AO)         #首先通知自身，我出攻击牌了.
		AO.target.Notify(HOOK_ATTACKED,AO)    #通知对象，被攻击了.
		if sgs.players.answer.Answer(AO):         #等待应答.
			AO.src.Notify(HOOK_ATTACKFAILED,AO) #杀失败了.
			return
		if AO.src.Notify(HOOK_ATTACKOK,AO):   #杀成功了,但是这个消息被其他修改了。比如寒冰剑.
			return
		AO.target.Damage(AO.src.damage) #许储少摸2张，伤害+1
		AO.target.Notify(HOOK_HURTED,AO,AO.src.damage) #通知这个玩家，你受到伤害了,而且还是受到了damage的伤害.
	def Dump(self):
		print "基础技能:",self.name
		print self.desc	
if __name__=="__main__":
	import sgs.players.answer
#	ShaObj().Dump()
	sgs.players.answer.Answer(1)
