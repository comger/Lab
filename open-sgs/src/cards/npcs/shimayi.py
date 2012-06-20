#!/usr/bin/env python
#coding: utf8

from sgs.cards.npc import NPC,MALE
from sgs.cards.cardkind import *
from sgs.triggers.trigger import HOOK_HURTED,HOOK_PANGDING
from sgs.aos.ao import AO
from sgs.players.command import *

class ShiMaYi(NPC):
	def __init__(self):
		NPC.__init__(self, "司马懿",3,MALE,"狼怨之魂！")
	def Apply(self,db):
		db.Hook(HOOK_HURTED,self)
		db.Hook(HOOK_PANGDING,self)
	def HOOK_HURTED(self,AO,damage):
		"""
			得到伤害自己的人的一张牌.
		"""
		print "司马懿受到攻击，获得对方一张牌的无赖技能发动"
		cmd = AO.target.getCmd()
		while (cmd.kind != CMD_SELECT) or (len(cmd.poslist) != 1):
			print "请选择要拿走的牌"
			cmd = AO.target.getCmd()	
		card = AO.src.lookCard(cmd.poslist)
		AO.src.Qi(cmd.poslist)
		AO.target.addCard(card[0])  #得到一张牌了
	def HOOK_PANGDING(self,card,player=None):
		if not player: return
		print "司马懿无赖技能篡改判定牌发送，可以直接U来选择自己的牌进行改变"
		cmd = player.getCmd()
		while cmd.kind == CMD_USE:
			if len(cmd.poslist) != 1:
				print "出太多牌了"
				cmd = player.getCmd()
				continue
			mecard = player.lookCard(cmd.poslist)
			player.Qi(cmd.poslist)
			card.CloneFrom(mecard[0])
			break
if __name__=="__main__":
	ShiMaYi().Dump()
