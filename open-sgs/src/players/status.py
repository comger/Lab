#!/usr/bin/env python
#coding: utf8

GAME_WAITING     = 0 #等待游戏的状态。等待游戏开始 or 自己已经出好牌了的状态.
GAME_START       = 1 #游戏开始阶段.
GAME_ROUND_START = 2 #个人回合开始阶段.
GAME_ROUND_END   = 3 #个人回合结束阶段.
GAME_PANDING     = 4 #判定阶段.
GAME_MOPAI       = 5 #摸牌，派牌阶段.
GAME_CHUPA       = 6 #出牌阶段.
GAME_QIPAI       = 7 #弃牌阶段.

class GameStatus(object):
	"""
		游戏的状态.
	"""
	CNT = 8
	def __init__(self):			self.flag = [True]* GameStatus.CNT
	def Disable(self,status):	self.flag[status]=False
	def DisableAll(self):		self.flag = [False]* GameStatus.CNT
	def Enable(self,status):	self.flag[status] = True
	def EnableAll(self):		self.flag = [True]* GameStatus.CNT
	def Reset(self):			self.flag = [True]* GameStatus.CNT
	def get(self,status):		return self.flag[status]