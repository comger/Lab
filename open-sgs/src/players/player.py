#!/usr/bin/env python
#coding: utf8

from sgs.triggers.trigger import *
from sgs.utils.cardop import getHeadCard,getTailCard,putHeadCard,putTailCard #完整的牌类
from sgs.aos.ao import *
from sgs.cards.npc import FEMALE,MALE
from sgs.cards.cardkind import *

from role import *
from command import *
from role import *
from status import GameStatus

class Player(object):
	"""
		玩家的信息
	"""
	def __init__(self,account,role,npc):
		"""
			account   : 用户的账号.
			role      : 角色 ROLE_xx.
			npc       : 武将卡的对象.
		"""
		self.account = account   #玩家的帐户.
		self.role = role         #玩家的角色.

		self.name = npc.name
		self.desc = npc.desc
		self.sex  = npc.sex

		self.life    = npc.life  #当前血
		self.maxlife = npc.maxlife    #最大血

		if self.role == ROLE_ZG:    #主公多一滴血.
			self.life += 1
			self.maxlife += 1

		self.damage = 1               #当前的杀伤力
		self.maxdamage = 1            #杀伤力				

		self.usekill = npc.usekill            #可用杀的次数
		self.dodge_range  = npc.dodge_range   #躲避距离
		self.attack_range = npc.attack_range  #攻击距离

		self.status  = GameStatus()           #当前的状态.这样不是出牌的时候点击的也不用管了.

		self.cards = getHeadCard(4)            #手牌，初始化的手拍是4张.
		self.wields= []                        #装备牌
		self.waiting = []                      #等待判定的牌(乐不思蜀，闪电之类的)
		self.effects =[]                       #持续效果的牌，会显示出来的。比如中毒效果。会自动消失、也可以驱散

		self.get_default_card_cnt = 2          #默认的一次模牌数目.
		self.get_card_cnt         = 2          #当前的模牌的数目.

		self.cmdqueue = cmdQueue()             #玩家的操作指令队列.
		#---------------------------------------------------		
		self.db = TriggerDB()
		npc.Apply(self.db)                     #开始注册这个角色的特殊技能等.
	#--------Command-----------------
	def getCmd(self):
		return self.cmdqueue.get()
	def pushCmd(self,cmd):
		return self.cmdqueue.push(cmd)
	#---------------------------------
	def addWaiting(self,card):                 #添加到待判定区
		self.waiting.append(card)
	def WieldedWeapon(self):
		"""
			返回装备了的武器.
		"""
		for x in self.wields:
			if isWeaponCard(x): return x
		return None
	def __wield(self,pos):
		"""
			将手牌中的pos位置的牌移动到装备区.
		"""
		acard = self.cards.pop(pos)
		unwield=[]
		ok = acard.ObjKind()
		if ok < CK_ARM:
			return      #非可以装备的武器的了.
		if isDecMaCard(acard):      #是减马,卸载前面的马.
			unwield =  [card for card in self.wields if isDecMaCard(card)]
			self.wields = [ card for card in self.wields if not isDecMaCard(card.ObjKind()) ]
		elif isAddMaCard(acard):   #是加马
			unwield =  [card for card in self.wields if isAddMaCard(card)]
			self.wields = [ card for card in self.wields if not isAddMaCard(card)]
		elif isWeaponCard(acard): #是武器，卸载前面的武器.
			unwield = [card for card in self.wields if isWeaponCard(card)]
			self.wields = [ card for card in self.wields if not isWeaponCard(card)]
		else:   #卸载防局
			unwield = [card for card in self.wields if isArmCard(card)]
			self.wields = [ card for card in self.wields if not isArmCard(card)]

		for card in unwield: card.unApply()
		acard.Apply(self,self.db)  #卡装备上.
		self.wields.append( acard )
		print "%s装备上%s" % (self.name,acard.obj.name)
	def Heal(self,heal):
		self.life += heal
		if self.life >= self.maxlife: self.life = self.maxlife	
	def Damage(self,damage):
		self.life -= damage
	def PowerHeal(self,heal):
		self.maxlife += heal
		self.life = self.maxlife
	def isliving(self):
		return self.life > 0
	def findCard(self,card):
		"""
			查找某张牌,返回在牌的位置.(from 0的)
		"""
		i = 0
		for x in self.cards:
			if x == card: return i
			i += 1
		for x in self.wields:
			if x == card: return i
			i += 1
		for x in self.waiting:
			if x == card: return i
			i += 1
		return -1
	def lookCard(self,poslist):
		"""
			返回pos位置处的牌.
			pos从0开始的.
		"""
		ret=[]
		cnt1 = len(self.cards)
		cnt2 = len(self.wields)
		cnt3 = len(self.waiting)
		cnt = cnt1+cnt2+cnt3
		for pos in poslist:
			if pos > cnt:  return None
			if pos < cnt1:  #手牌
				ret.append(self.cards[pos])
			elif pos < cnt1+cnt2: #装备:
				ret.append(self.wields[pos-cnt1])
			else: #判定牌
				ret.append(self.waiting[pos-cnt1-cnt2])
		return ret
	def addCard(self,card):
		"""
			得到一张额外的牌
		"""
		self.cards.append(card)
	def getExtraCard(self,cnt):
		"""
			摸指定多的牌
		"""
		card = getHeadCard(cnt)
		self.cards.extend(card)
	def getCard(self):
		"""
			摸牌了
		"""
		card = getHeadCard(self.get_card_cnt)
		self.cards.extend(card)

	def UseSkill(self,target,i):
		"""
			特殊技能出牌.
		"""
		card = self.cards[i]
		try:
			ao = AO(self,target,card,card.obj.getReq())
		except:
			ao = AO(self,target,card,None)
		if not self.Notify(HOOK_SKILL,ao):
			print "不需瞎用" 
			return
		ao.card.Apply(ao) #牌可能被换掉了的
		self.cards.pop(i)
	def Chu(self,target,i):
		"""
			出牌,只能出手牌的.
			一次只能是一张的.
		"""
		if i >= len(self.cards):
			print "只能出手牌的阿"
			return
		card = self.cards[i]
		 #武器类的了
		if card.ObjKind() >= CK_ARM:
			self.__wield(i)
		elif card.ObjKind() >= CK_SPELL: #法术类的
			ao = AO(self,target,card,card.obj.getReq())
			card.Apply(ao)
		elif card.ObjKind() == CK_SHA:   #杀
			if (self.usekill < 1):
				print "还杀阿,放下屠刀，立地成佛!"
				return
			self.usekill -= 1
			self.cards.pop(i)
			ao = AO(self,target,card,card.obj.getReq())
			card.Apply(ao)
		elif card.ObjKind() == CK_SHAN:  #闪
			print "平白无故，闪什么?"
		else:
			if target != self:
				print "你要给对方加血?"
			else:
				self.cards.pop(i)
				ao = AO(self,target,card,None)
				card.Apply(ao)				
	def Qi(self,poslist):
		"""
			丢弃牌. poslist.
		"""
		poslist.sort(reverse=True) #按照从大到小的顺序排列
		cnt1 = len(self.cards)
		cnt2 = len(self.wields)
		cnt3 = len(self.waiting)
		cnt = cnt1+cnt2+cnt3
		for x in poslist:
			if x < cnt1:  #手牌
				del self.cards[x]
			elif x < cnt1+cnt2: #装备牌
				self.wields[x-cnt1].unApply() #需要进行反安装的
				del self.wields[x-cnt1]
			else:
				del self.waiting[x-cnt1-cnt2]
	def Finish(self):
		"""
			回合结束.需要检查手牌的数目.
		"""
		self.usekill = 1                #复原了
		if self.Notify(HOOK_ROUND_END): return #通知自己，回合结束了.有些特殊技能就可以跳过检查手牌的.比如吕蒙.
		print "弃牌检查未实现"
	def DisableHook(self,hookid):
		self.db.Disable(hookid)
	def EnableHook(self,hookid):
		self.db.Enable(hookid)
	def Notify(self,hookevt,*sth,**another):
		"""
			被通知hookevt事件发生了.
			默认返回False,有些Notify需要返回一些结果的。比如: Finish时.
		"""
		print self.name,"Notified",getEVTName(hookevt)
		hook = self.db.getHook(hookevt)
		if not hook: return False
		r = False
		for cardobj in hook:
			try:
				method = getattr(cardobj,getEVTName(hookevt))
				if method(*sth,**another): r = True
			except Exception,msg:
				print msg
		return r
#=============================信息交流部分=====================================================





#=============================显示============================================================
	def HP(self):
		"""
			显示基本信息
		"""
		print "帐户:",self.account,"\t身份:",RoleName(self.role)
		
		sex="男"
		if self.sex == FEMALE: sex="女"
		print "角色名:",self.name,"\t",sex,"\t最大气血:",self.maxlife,"\t当前气血:",self.life
		print "杀可用次数:",self.usekill,"\t躲避距离:",self.dodge_range,"\t攻击距离:",self.attack_range
		
		print "手牌:"
		i=0
		for x in self.cards:
			print "\t","%s(%d)" % (x,i)
			i += 1
		
		print "已装备牌:"
		for x in self.wields:
			print "\t","%s(%d)" % (x,i)
			i += 1
		print "待判定牌:"
		for x in self.waiting:
			print "\t","%s(%d)" % (x,i)
			i += 1
		print "========================================================"
	def Dump(self): self.HP()
	
if __name__=="__main__":
	pass
