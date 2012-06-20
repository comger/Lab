#!/usr/bin/env python
#coding: utf8

from random import shuffle
from cardkind import *
from card import HEITAO,HONGTAO,MEIHUA,FANGKUAI,Card

from base.sha import ShaObj
from base.shan import ShanObj
from base.tao import TaoObj

from arms.bgz import BgzObj
from arms.rwd import RwdObj

from weapons.qlyyd import QlyydObj
from weapons.zgln import ZglnObj
from weapons.hbj import HbjObj
from weapons.qgj import QgjObj
from weapons.gsf import GsfObj

from spells.ghcq import GhcqObj
from spells.wxkj import WxkjObj
from spells.ssqy import SsqyObj
from spells.wjqf import WjqfObj
from spells.wzsy import WzsyObj
from spells.jd import JdObj
from spells.nmrq import NmrqObj
from spells.tyjy import TyjyObj
from spells.wgfd import WgfdObj

from horses.jy import JyObj

from sgs.resource.vars import GameVar

def CreateFakeCards(point,objclass):
	return [
		Card(point,HEITAO,objclass()),
		Card(point,HONGTAO,objclass()),
		Card(point,MEIHUA,objclass()),
		Card(point,FANGKUAI,objclass())
		]
def CreatCardList():
	ret = []
	ret.extend(CreateFakeCards(1,ShaObj))  #杀
	ret.extend(CreateFakeCards(2,ShanObj)) #闪
	ret.extend(CreateFakeCards(3,TaoObj))  #桃
	ret.extend(CreateFakeCards(4,BgzObj))  #八卦阵
	ret.extend(CreateFakeCards(5,QlyydObj)) #青龙偃月刀
	ret.extend(CreateFakeCards(6,GhcqObj))  #过河拆桥
	ret.extend(CreateFakeCards(7,WxkjObj))  #无懈可击
	ret.extend(CreateFakeCards(8,SsqyObj))  #顺手牵羊
	ret.extend(CreateFakeCards(9,WjqfObj))  #万箭齐发
	ret.extend(CreateFakeCards(10,WzsyObj)) #无中生有
	ret.extend(CreateFakeCards(11,JdObj))   #决斗 
	ret.extend(CreateFakeCards(12,ZglnObj)) #诸葛连弩
	ret.extend(CreateFakeCards(13,JyObj))   #绝影
	ret.extend(CreateFakeCards(14,NmrqObj)) #南蛮入侵
	ret.extend(CreateFakeCards(15,TyjyObj)) #桃园结义
	ret.extend(CreateFakeCards(16,RwdObj))  #仁王盾
	ret.extend(CreateFakeCards(17,WgfdObj)) #五谷丰登
	ret.extend(CreateFakeCards(18,HbjObj))  #寒冰剑
	ret.extend(CreateFakeCards(19,QgjObj))  #青釭剑
	ret.extend(CreateFakeCards(20,GsfObj))  #贯石斧
	return ret
CardList= CreatCardList()

class WholeCard(object):
	"""
		一副牌，用来发牌和洗牌的.
	"""
	def __init__(self):
		poslist = range(len(CardList))
		shuffle(poslist)  #对这些进行洗牌.
		self.cards = [ CardList[pos] for pos in poslist ]
	def __refresh(self):
		"""
			1.去除玩家手上的牌＆装备牌&等待判定的牌
			2.去除现存的牌.
		"""
		existids =[]
		if GameVar:
			for player in GameVar.getLivingPlayer():
				existids.extend([card.id for card in player.cards])
				existids.extend([card.id for card in player.wields])
				existids.extend([card.id for card in player.waiting])
		existids.extend( [card.id for card in self.cards] )
		available = [card for card in CardList if card.id not in existids]

		poslist = range(len(available))
		shuffle(poslist)  #对这些进行洗牌.
		temp = [ available[pos] for pos in poslist ]
		self.cards.extend(temp)  #OK了.
	def getHead(self,cnt):
		"""
			摸牌,从牌顶摸.
			返回的结果是:
			[ card ]
		"""
		if len(self.cards) < cnt: self.__refresh()
		if len(self.cards) < cnt: raise Exception("牌不足了，牌都在手上了！")
		ret = self.cards[:cnt]
		del self.cards[:cnt]
		return ret
	def getTail(self,cnt):
		"""
			摸牌,从牌底摸.
			返回的结果是:
			[ card ]
		"""
		if len(self.cards) < cnt: self.__refresh()
		if len(self.cards) < cnt: raise Exception("牌不足了，牌都在手上了！")
		ret = self.cards[-cnt:]
		del self.cards[-cnt:]
		return ret
	def putHead(self,cardlist):
		"""
			放回到牌顶
			cardlist: [ card ]
		"""
		i= 0
		for card in cardlist:
			self.cards.insert(i,card)
			i += 1
	def putTail(self,cardlist):
		"""
			放回到牌顶
			cardlist: [ card ]
		"""
		for card in cardlist: self.cards.append(pos)
	def Dump(self):
		for x in self.cards:
			print x.id,
		print ""
if __name__=="__main__":
	c = WholeCard()
	i = 7
	while i > 0:
		c.Dump()
		v=c.getHead(3)
		for x in v:
			print x.id,
		print "--->"
		i -= 1
	print "--------------"
	v = c.getHead(3)
	for p in v:
		print p.id,
	print "--------------"
	c.Dump()
	print "--------------"
	c.putHead(v)
	c.Dump()
