#!/usr/bin/env python
#coding: utf8

"""
	模拟器.
"""
from sgs.players.player import * 
from sgs.cards.npcs.ganning import *
from sgs.cards.npcs.lvbu import *
from sgs.cards.npcs.shimayi import *

from sgs.players.command import *
from sgs.resource.vars import GameVar
#---模拟部分的-----
def run():
	p1 = Player("player1",ROLE_ZG,ShiMaYi())
	p2 = Player("player2",ROLE_FZ,GanNing())
	GameVar.SetPlayList([p1,p2])
	
	cur = GameVar.curplayer()
	n = GameVar.nextplayer()
	cur.getCard()
	while True:
		print "===============>Round<================="
		cur.HP()
		n.HP()
		cmd = cur.getCmd()
		if cmd.kind == CMD_USE:
			if len(cmd.poslist) != 1:
				print "出太多牌了"
				continue
			cur.Chu(cmd.target,cmd.poslist[0])
		elif cmd.kind == CMD_USE_SKILL:
			if len(cmd.poslist) != 1:
				print "出太多牌了"
				continue
			cur.UseSkill(cmd.target,cmd.poslist[0])
		elif cmd.kind == CMD_DROP:
			cur.Qi(cmd.poslist) #弃牌了
		elif cmd.kind == CMD_HP:
			cur.HP()
			n.HP()
		elif cmd.kind == CMD_FIN:
			cur.Finish()
			if not n.isliving():
				print "Game Over","%s @ %s 获胜" % (cur.account,cur.name)
				break
			cur = n
			cur.getCard()
			n = GameVar.nextplayer()

if __name__=="__main__":
	run()
