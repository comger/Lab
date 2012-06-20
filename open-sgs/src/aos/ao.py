#!/usr/bin/env python
#coding: utf8

class AO(object):
	"""
		动作对象
	"""	
	def __init__(self,src_player,target_player,card_obj,req_obj,third_player=None):
		"""
			src_player: 动作的发起者
			target_player: 动作的目标,也就是接受者
			thirdtarget: 第3方受害者.比如： 借刀杀人.
			card_obj:   卡片本色对象
			req_obj:    要应答这个卡片可能的需求. AOReqItem或者AOReq_OR或者AOReq_AND
		"""
		self.src = src_player
		self.target = target_player
		self.thirdtarget = third_player
		self.card = card_obj #被拿张牌伤害的.
		self.req = req_obj #一旦req消失，就说明应对完成了。成功了。
	def Answered(self):
		"""
			是否已经达到应答的需求的了.
		"""
		if (not self.req) or (self.req.Matched()): return True
		return False

class AOReq(object):
	"""
		应答请求.
		需要满足:
		0. 是否已经匹配完成.
		1. 全部匹配的需求
		2. 是否可以部分匹配的需求，因为有些还需要判定的.
		3. 部分匹配部分的需求.
		4. 克隆用法
		----------------------------------------------------
		4. 某些情况下，次数的增加  or 针对某一类事件次数的增加.
		5. 需求次数的减少 or 针对某一类事件，次数的减少 .
		上述的2种可以通过返回的具体类来实现的了.通过Change方法.
		--> 同一类时间只能一次，就算是重复交叉的也不行.
	"""
	def __init__(self):
		self.marked = False
	def Matched(self):
		if self.marked: return 1#是否匹配结束了.
		return 0
	def Match(self,cardlist):return False  #完全匹配一个card列表,
	#-----需求的部分-----
	def RequireKind(self,kind):   return []  #需求中是否有kind这个花色的需求?返回具体的这个类
	def RequirePoint(self,point): return []  #需求中是否有point这个点数的需求?返回具体的这个类
	def RequireItem(self,item):   return []  #需求中是否有item这个牌对象的需求?杀，闪，之类。返回具体的这个类
	def RequireCard(self,card):   return []  #需求中是否有card这个对象的需求?以上三种的.
	
	def Mark(self):   self.marked = True       #标记这个对象.
	def unMark(self): self.marked = False      #取消标记这个对象.
	def Clone(self):  pass					   #克隆用法，比如对群体性法术等.
class AOReqKind(AOReq):
	"""
		针对花色的
	"""
	def __init__(self,kind):
		super(AOReqKind,self).__init__()
		self.kind = kind     #花色
	def Match(self,cardlist):
		if (not cardlist) or len(cardlist) != 1: return False
		if self.Matched(): return False
		for x in cardlist:
			if x.kind != self.kind: return False
		return True
	def RequireKind(self,kind):
		if self.Matched(): return []
		if kind != self.kind: return []
		return [self]
	def RequireCard(self,card):
		if self.Matched(): return []
		if card.kind != self.kind: return []
		return [self]
	def Clone(self):
		return AOReqKind(self.kind)
	def __str__(self):
		return "AOReqKind:"+str(self.kind)
	
class AOReqPoint(AOReq):
	"""
		针对牌的点数的。
	"""
	def __init__(self,point):
		super(AOReqPoint,self).__init__()
		self.point = point	#卡片的点数
	def RequirePoint(self,point):
		if self.Matched(): return []
		if self.point != point: return []
		return [self]
	def RequireCard(self,card):
		if self.Matched(): return []
		if card.point != self.point: return []
		return [self]
	def Match(self,cardlist):
		if (not cardlist) or len(cardlist) != 1: return False
		if self.Matched(): return False
		for x in cardlist:
			if x.point != self.point: return False
		return True
	def Clone(self):
		return AOReqPoint(self.point)
	def __str__(self):
		return "AOReqPoint:"+str(self.point)

class AOReqItem(AOReq):
	"""
		单个的需求应答,针对牌的种类的。
	"""
	def __init__(self,item):
		super(AOReqItem,self).__init__()
		self.item = item
	def RequireItem(self,item):
		if self.Matched(): return []
		if self.item != item: return []
		return [self]
	def RequireCard(self,card):
		if self.Matched(): return []
		if card.ObjKind() != self.item: return []
		return [self]
	def Match(self,cardlist):
		"""
			匹配时候成功与否.
			cardlist中按照id排好序的。这个id是种别id.比如所有的桃是一个id.
		"""
		if (not cardlist) or len(cardlist) != 1: return False
		if self.Matched(): return False
		for x in cardlist:
			if x.ObjKind() != self.item : return False
		return True
	def Clone(self):
		return AOReqItem(self.item)
	def __str__(self):
		return "AOReqItem:"+str(self.item)

#--------------------------------------------------------------------------------------------------
class AOReq_AND(object):
	"""
		动作中的应答的需求.
	"""
	def __init__(self):
		"""
			必须满足content中的全部项，就认为这个动作被成功应答了。
		"""
		self.content=[]
	def Append(self,req):
		"""
			增加一个可以满足这个动作的需求项req.
			req可以是: AOReqItem,AOReqKind,AOReqPoint.AOReq_AND.AOReq_OR
		"""
		self.content.append(req)
	def Matched(self):
		c = 0
		for x in self.content:
			v = x.Matched()
			if v < 1: return 0
			c += v
		return c
#	def Mark(self): pass
#	def unMark(self): pass	
	def RequireCard(self,card):
		ret = []
		for x in self.content:
			t = x.RequireCard(card)
			if t: ret.extend(t)
		return ret
	def RequireKind(self,kind):
		ret=[]
		for x in self.content:
			t = x.RequireKind(kind)
			if t: ret.extend(t)
		return ret
	def RequirePoint(self,point):
		ret = []
		for x in self.content:
			t = x.RequirePoint(point)
			if t: ret.extend(t)
		return ret
	def RequireItem(self,item):
		ret=[]
		for x in self.content:
			t = x.RequireItem(item)
			if t: ret.extend(t)
		return ret
	def Match(self,cardlist):
		"""
			全排列的匹配的了.
		"""
		def getmaybelist(acardlist): #得到全部可能的值.
			ret= []
			for card in acardlist:
				m = []
				for x in self.content:
					t = x.RequireCard(card)
					if t: m.extend(t)
				if not m: return []
				ret.append(m)
			return ret
		def trysth(maybelist):
			#--其实是得到一个maybelist的排列组合了--
			#[ [1,2,3],[0,1,2],[3,4],[1,2] ]
			for f in maybelist[0]:
				if f.Matched(): continue
				f.Mark()
				if not maybelist[1:]:
					yield [f]					
				else:
					for s in trysth(maybelist[1:]):
						m = [f]
						m.extend(s)
						yield m 
				f.unMark()				
		if not cardlist: return False
		mlist = getmaybelist(cardlist)
		if not mlist: return False
		#--准备开始排列组合了--
		for q in trysth(mlist):
			if self.Matched() != len(cardlist): continue
			return True
		return False
	def Clone(self):
		ret = AOReq_AND()
		ret.content = self.content[:]
		return ret
class AOReq_OR(object):
	"""
		必须满足content中的一项，就认为这个动作被成功应答了。
			比如说:
			万箭齐发动作中，需要"闪"或者"无懈可击"
			一旦满足其中一项，都可以的了。
			比如:
			  两个闪.content=[ [闪，闪] ] 就是说必须出2个闪才能满足.
			  两个闪.content=[ [闪，闪],无懈可击 ] 就是说必须出2个闪才能满足.
	"""
	def __init__(self):
		self.content=[]
	def Append(self,req):
		"""
			增加一个可以满足这个动作的需求项req.
			req可以是: AOReq_AND,AOReqItem,AOReq_OR. 这样就可以实现组合效应的了.
		"""
		self.content.append(req)
	def Matched(self):
		for x in self.content:
			v = x.Matched()
			if v > 0: return v
		return 0
#	def Mark(self): pass
#	def unMark(self): pass
	def RequireCard(self,card):
		ret=[]
		for x in self.content:
			t = x.RequireCard(card)
			if t: ret.extend(t)
		return ret
	def RequireKind(self,kind):
		ret = []
		for x in self.content:
			t = x.RequireKind(kind)
			if t: ret.extend(t)
		return ret
	def RequirePoint(self,point):
		ret=[]
		for x in self.content:
			t = x.RequirePoint(point)
			if t: ret.extend(t)
		return ret
	def RequireItem(self,item):
		ret=[]
		for x in self.content:
			t = x.RequireItem(item)
			if t: ret.extend(t)
		return ret
	def Match(self,cardlist):
		"""
			全排列的匹配的了.
		"""
		def getmaybelist(acardlist): #得到全部可能的值.
			ret= []
			for card in acardlist:
				m = []
				for x in self.content:
					t = x.RequireCard(card)
					if t: m.extend(t)
				if not m: return []
				ret.append(m)
			return ret
		def trysth(maybelist):
			#--其实是得到一个maybelist的排列组合了--
			#[ [1,2,3],[0,1,2],[3,4],[1,2] ]
			for f in maybelist[0]:
				if f.Matched(): continue
				f.Mark()
				if not maybelist[1:]:
					yield [f]
				else:
					for s in trysth(maybelist[1:]):
						m = [f]
						m.extend(s)
						yield m 
				f.unMark()
		if not cardlist: return False
		mlist = getmaybelist(cardlist)
		if not mlist: return False
		#--准备开始排列组合了--
		for alist in trysth(mlist):
			if self.Matched() != len(cardlist): continue
			return True
		return False		
	def Clone(self):
		sth = AOReq_OR()
		sth.content = self.content[:]
		return sth
	
if __name__=="__main__":
	from sgs.cards.card import HEITAO,Card
	from sgs.cards.cardkind import *
	from sgs.cards.base.sha import ShaObj
	from sgs.cards.base.shan import ShanObj
	req = AOReq_OR()
	A = AOReq_AND()
	A.Append(AOReqKind(HEITAO))
	A.Append(AOReqItem(CK_SHA))
	req.Append(A)
	req.Append(AOReqItem(CK_SHA))
	print req.Matched()
	#print req.Match([Card(4,HEITAO,ShanObj()),Card(2,HEITAO,ShaObj()),Card(2,3,ShaObj())])
	print req.Match([Card(2,HEITAO,ShaObj())])
