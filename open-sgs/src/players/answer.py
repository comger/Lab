#!/usr/bin/env python
#coding: utf8

from command import CMD_USE,CMD_DROP,CMD_FIN,CMD_USE_SKILL

def Answer(AO):
	"""
		AO的target应答这个动作.
		True:  应对成功.
		False: 应对失败.
	"""
	if AO.Answered(): return True  #已经应对结束了. :)
	print "如果%s无牌可应对,则直接返回" % AO.target.name
	player = AO.target
	req = AO.req
	cmd = player.getCmd()
	while cmd.kind != CMD_FIN:
		if cmd.kind in [CMD_USE,CMD_USE_SKILL]:
			cardlist = player.lookCard(cmd.poslist)
			if cardlist:
				if req.Match(cardlist):
					player.Qi(cmd.poslist) #丢弃掉这些牌的了.
					return True
				print player.name,"应对错误，重新选择牌出"
		cmd =  AO.target.getCmd()
	return False

def Answer_Return(AO):
	"""
		AO的target应答这个动作.
		(flag,card)
		flag->True:  应对成功.
		      cardlist:  用什么牌应对成功的也顺便返回了.
		flag->False: 应对失败.
	"""
	if AO.Answered(): return (True,None)  #已经应对结束了. :)
	print "如果%s无牌可应对,则直接返回" % AO.target.name
	player = AO.target
	req = AO.req
	cmd = player.getCmd()
	while cmd.kind != CMD_FIN:
		if cmd.kind in [CMD_USE,CMD_USE_SKILL]:
			cardlist = player.lookCard(cmd.poslist)
			if cardlist:
				if req.Match(cardlist):
					player.Qi(cmd.poslist) #丢弃掉这些牌的了.
					return (True,cardlist)
				print player.name,"应对错误，重新选择牌出"
		cmd =  AO.target.getCmd()
	return (False,None)