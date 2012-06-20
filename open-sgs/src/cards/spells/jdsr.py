#!/usr/bin/env python
#coding: utf8

from sgs.cards.cardkind import *
from sgs.cards.spell import Spell
from sgs.triggers.trigger import *
import sgs.players.answer
from sgs.resource.vars import GameVar
from sgs.aos.ao import AOReqItem,AOReq_OR,AOReq_AND
class JdObj(Spell):
	"""
		借刀杀人
	"""	
	kind = CK_JDSR
	def __init__(self):
		Spell.__init__(self,"借刀杀人","敌已明，友未定，引友杀敌，不自出力，以《损》推演  ---<三十六计>")
	def Apply(self,AO):
		card = AO.target.isWieldWeapon()
		if not card:
			print "对方没武器在手啊"
			return
		if not AO.thirdtarget:
			print "借刀杀人总的有个目标吧？"
			return
		i = AO.src.findCard(AO.card)
		if i < 0: raise Exception("卡不见了")
		AO.src.Qi([i])  #丢掉这张牌了.
		
		target = AO.target
		cmd = target.getCmd()
		poslist = cmd.poslist
		
		
		
		AO.src.Notify(HOOK_SPELL,AO)           #首先通知自身，我出法术攻击牌了.
		(flag,cardlist) =  sgs.players.answer.Answer_Return(AO) #应对并返回应对的牌.
		if not flag:  #如果应对失败
			AO.target.Damage(1)
			AO.target.Notify(HOOK_HURTED,AO,1) #通知这个玩家，你受到伤害了,而且还是受到了damage的伤害.
			return
		if len(cardlist) == 1 and cardlist[0].ObjKind() == CK_WXKJ: #应对成功，但是是无懈可击应对的.
			AO.src.Notify(HOOK_SPELLFAILED,AO) #法术攻击失败了.
			return
		
		reqlist=[]
		for x in cardlist: reqlist.append(AOReqItem(x.ObjKind()))
		if len(reqlist) > 1:
			req = AOReq_AND()
			for r in reqlist: req.Append(r)
			AO.req = req
		else:
			AO.req = reqlist[0]
		T = [(AO.src,AOReqItem(CK_SHA)),(AO.target,AO.req)]
		i = 0 
		while True: #无限死循环应答了.
			AO.src    = T[ (i+1) % 2][0]
			AO.target = T[ i % 2][0]
			AO.req    = T[i % 2][1].Clone()
			if not sgs.players.answer.Answer(AO): break #应答失败的.
			i += 1
		AO.target.Damage(1)
		AO.target.Notify(HOOK_HURTED,AO,1) #通知这个玩家，你受到伤害了,而且还是受到了damage的伤害.
if __name__=="__main__":
	pass
