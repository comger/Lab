#!/usr/bin/env python
#coding: utf8

"""
 	玩家的操作指令队列.
 	现在是模拟部分：
 	
 	
	用户指令分析:
	指令如下格式:
	CMD xxx xxx
	使用牌:
	U 1 3        用位置1的牌作用与player3上面。保护直接也这样
				 装备的时候，无视player这个选项了 
	D 1          丢弃位置1的牌
	D 1 2 3 4 5  丢弃位置1,2,3,4,5的牌
	F            回合结束
	SU 1         使用位置1的牌，并且加上了特殊技能.
	S 1          选择某个位置的牌
	             比如: 甘宁任意黑色牌可以作[过河拆桥]。万一是黑色杀呢？
	Q            退出了
"""
from sgs.resource.vars import GameVar,NetVar
import sys

CMD_USE  = 0
CMD_DROP = 1
CMD_FIN  = 2
CMD_USE_SKILL = 3 #SU
CMD_SELECT = 4    #选牌.

CMD_HP   = 5  #显示自身的状态

CMD_QUIT = 100 #退出
class cmd(object):
	CMD_MAPER={
			CMD_USE : 'CMD_USE',
			CMD_DROP : 'CMD_DROP',
			CMD_FIN : 'CMD_FIN',
			CMD_USE_SKILL : 'CMD_USE_SKILL',
			CMD_SELECT : 'CMD_SELECT',
			CMD_HP : 'CMD_HP',
			CMD_QUIT : 'CMD_QUIT',
	}
	def __init__(self,kind,poslist,target=None):
		"""
			kind: 指令类别
			poslist: 第几张牌，或者牌的列表
			target: 对谁操作?player.
		"""
		self.kind = kind
		self.poslist = poslist
		self.target = target
	def __str__(self):
		return "%s:%s:%s" % (self.CMD_MAPER.get(self.kind,"UNKNOWN CMD"),self.poslist,self.target)

class cmdQueue(object):
	"""
		玩家的指令队列.
	"""
	def __init__(self):
		self.queue = []
	def __parse(self):
		input=""
		try:
			input = raw_input('?')
			cmds = input.split()
			if not cmds: return None
			c = cmds[0].upper()
			if c == 'U':
				target = GameVar.getPlayer(int(cmds[-1]))
				return cmd(CMD_USE,map(int,cmds[1:-1]),target)
			if c == 'US':
				target = GameVar.getPlayer(int(cmds[-1]))
				return cmd(CMD_USE_SKILL,map(int,cmds[1:-1]),target)
			if c == 'D':	return cmd(CMD_DROP,map(int,cmds[1:]))
			if c == 'F':
				if len(cmds) != 1: raise Exception("结束还要出牌?")
				return cmd(CMD_FIN,None)
			if c == 'S':
				return cmd(CMD_SELECT,map(int,cmds[1:]))
			if c == 'HP':
				return cmd(CMD_HP,None)
			if c == 'Q':
				print "Quit Game...."
				return cmd(CMD_QUIT,None)
		except Exception,e:
			print "CMD Parse Error:",input
			print e
			return None
	def get(self):
		"""
			得到指令.
		"""
		if self.queue: return self.queue.pop(0)
		while True:
			try:
				c = self.__parse()
				if c:
					if c.kind != CMD_QUIT: return c
					break
			except:
				pass
		sys.exit(0)

	def push(self,cmd):
		"""
			将一个命令重新的回退回来.
		"""
		self.queue.insert(0, cmd)
		
if __name__=="__main__":
	Q = cmdQueue()
	print Q.get()
