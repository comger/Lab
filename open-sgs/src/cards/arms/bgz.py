#!/usr/bin/env python
#coding: utf8

"""
	八卦阵
"""
from sgs.triggers.trigger import HOOK_ATTACKED,HOOK_PANGDING
from sgs.cards.cardkind import *
from sgs.cards.arm import Arm
from sgs.cards.card import HONGTAO,FANGKUAI
from sgs.resource.vars import GameVar
import sgs.utils.cardop

class BgzObj(Arm):
	"""
		八卦阵
	"""
	kind = CK_BGZ
	def __init__(self):
		Arm.__init__(self,"八卦阵","乾三连，坤六断，震仰盂，艮覆碗，离中虚，坎中满，兑上缺，巽下断")
	def Apply(self,player,db):
		"""
			安装需要出闪的时候的钩子.
		"""
		self.db = db
		self.player = player
		self.db.Hook(HOOK_ATTACKED,self)
	def unApply(self):
		if not self.db: return
		#--从player中去除掉这个装备--
		self.db.unHook(HOOK_ATTACKED,self)
	def HOOK_ATTACKED(self,AO):
		if AO.Answered(): return   #已经匹配成功的了.
		aoreq = AO.req.RequireItem(CK_SHAN)
		if not aoreq: return       #闪不起作用的.
		cardlist = sgs.utils.cardop.getHeadCard(1)
		card = cardlist[0]
		print "判定牌是:",card
		GameVar.NotifyAll(HOOK_PANGDING,card) #需要通知全部人了，因为司马懿是可以篡改自己的
		#--------------------------------------------------
		if card.kind in [HONGTAO,FANGKUAI]:
			aoreq[0].Mark()  #设定标记结束的了
			if AO.Answered(): AO.req = None #就忽略这个请求了.
if __name__=="__main__":
#	BgzObj().Dump()
	b = BgzObj()
	method = getattr(b,'HOOK_ATTACKED')
	print method
