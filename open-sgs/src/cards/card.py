#!/usr/bin/env python
#coding: utf8

from sgs.utils.uid import getUID

HEITAO   = 1 #黑桃
HONGTAO  = 2 #红桃
MEIHUA   = 3 #梅花
FANGKUAI = 4 #方块

KIND_MAP={
		HEITAO : '黑桃',
		HONGTAO : '红桃',
		MEIHUA : '梅花',
		FANGKUAI : '方块'
}
def getCardKind(kind): return KIND_MAP.get(kind,"未知花色")

class Card(object):
	"""
		所有纸牌的模板。
	"""
	def __init__(self,point,kind,obj):
		self.point = point  #纸牌的点数.
		self.kind  = kind   #纸牌的花色.
		self.obj   = obj    #牌面上的物体，以便使用或者发挥功效.
		self.id    = getUID()
	def ObjKind(self): return self.obj.kind
	def CloneFrom(self,card):
		"""
			将自身变成card一样的.
		"""
		self.point = card.point
		self.kind = card.kind
		self.obj = card.obj
	def Apply(self,*sth):
		"""
			出牌发挥功效的函数.
			sth:
			对于arm类来说是player和db.装备钩子用
			对于spell来说是AO
			对于杀,闪,桃来说是AO
		"""
		return self.obj.Apply(*sth)
	def unApply(self):
		"""
			卸载牌。自针对arm有用.
		"""
		self.obj.unApply()
	def __str__(self):
		return "%s%d(%s)" % (getCardKind(self.kind),self.point,self.obj.name)
	def Dump(self):
		print "卡片:",getCardKind(self.kind),self.point,'-->',self.obj.name
if __name__=="__main__":
		pass
