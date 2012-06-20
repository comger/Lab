#!/usr/bin/env python
#coding: utf8

"""
	游戏进程.
"""

class Game(object):
	def SetPlayList(self,playerlist):
		"""
			playerlist: 玩家列表
		"""
		self.playerlist = [ (player,True) for player in playerlist ]
		self.cur = 0
		self.cnt = len(self.playerlist)
	def curplayer(self):
		"""
			得到当前的玩家
		"""
		player,living = self.playerlist[self.cur % self.cnt]
		if not living: raise Exception("get Dead Player?") 
		return player
	def nextplayer(self):
		"""
			下一个玩家.
		"""
		v = 0
		while True:
			self.cur += 1
			player,living = self.playerlist[self.cur % self.cnt]
			if living: return player
			v += 1
			if v >= 50: break
		raise Exception("Maybe @ Game next Loop")
	def killplayer(self,player):
		i = 0
		while i < self.cnt:
			if self.playerlist[i][0] == player:
				self.playerlist[i][1] = False
				break
			i += 1
	def getPlayer(self,pos):
		"""
			得到指定位置的玩家.
		"""
		if pos <  0: raise Exception("getPlayer_Pos ,pos <0")
		if pos > self.cnt: raise Exception("getPlayer_Pos ,pos > self.cnt")
		if pos == 0: return self.curplayer()
		pos -= 1
		player,living = self.playerlist[pos]
		if not living: raise Exception("getPlayer_Pos,你要返回死人？")
		return player
	def getLivingPlayer(self):
		"""
			得到全部存活的玩家.
		"""
		return [ player for player,living in self.playerlist if living]
	def getOtherPlayer(self,me):
		"""
			得到除自己外的全部玩家.
		"""
		pos = self.__getplayerpos(me)
		if pos == -1: raise Exception("getOtherPlayer失败")
		i = (pos+1) % self.cnt
		ret = []
		while i != pos:
			player,living =  self.playerlist[i]
			if living: ret.append(player)
			i += 1
			i %= self.cnt
		return ret
	def getPlayerCount(self):
		"""
			玩家数目
		"""
		i = 0
		for player,living in self.playerlist:
			if living: i +=1
		return i
	def Start(self):
		"""
			游戏开始了
		"""
		pass
	def __getplayerpos(self,aplayer):
		i = -1
		for player,living in self.playerlist:
			i += 1
			if living and (player == aplayer): return i
		return -1
	def NotifyOther(self,me,*sth):
		"""
			通知其他的玩家.
		"""
		pos = self.__getplayerpos(me)
		if pos == -1: raise Exception("你要通知谁？")
		i = (pos+1) % self.cnt
		while i != pos:
			player,living =  self.playerlist[i]
			if living: player.Notify(*sth,player=player)
			i += 1
			i %= self.cnt
	def NotifyAll(self,*sth):
		"""
			通知全部玩家.
		"""
		for player,living in self.playerlist:
			if not living: continue
			player.Notify(*sth,player=player)