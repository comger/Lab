#!/usr/bin/env python
#coding: utf8

from sgs.cards.cardkind import CK_WGFD
from sgs.cards.spell import Spell
from sgs.triggers.trigger import *
from sgs.resource.vars import GameVar
from sgs.players.command import CMD_SELECT
import sgs.utils.cardop

class WgfdObj(Spell):
	"""
		五谷丰登
	"""	
	kind = CK_WGFD
	def __init__(self):
		Spell.__init__(self, "五谷丰登", "是故风雨时节，五谷丰熟，社稷安宁 ---六韬.龙韬.立将")
	def Apply(self,AO):
		i = AO.src.findCard(AO.card)
		if i < 0: raise Exception("卡不见了")
		AO.src.Qi([i])  #丢掉这张牌了.
		
		cnt = GameVar.getPlayerCount()
		cardlist = sgs.utils.cardop.getHeadCard(cnt)
		players = GameVar.getLivingPlayer()
		i = 0
		for player in players:
			if player == AO.src: break
			i += 1
		xs = players[i:]
		xs.extend(players[:i]) #顺序好了.
		for player in xs:
			i = 0
			for card in cardlist:
				print "%s(%d)" % (card,i)
				i += 1
			print "请%s挑选" % player.name
			cmd = player.getCmd()
			while (cmd.kind != CMD_SELECT) or (len(cmd.poslist) !=1) or (cmd.poslist[0] >= i):
				print "%s选择出错，请选择"
				cmd = player.getCmd()
			
			card =cardlist.pop(cmd.poslist[0])
			player.addCard(card)
if __name__=="__main__":
	pass
