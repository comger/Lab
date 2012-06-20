#!/usr/bin/env python
#coding: utf8

HOOK_START       = 1 #游戏开始阶段
HOOK_ROUND_START = 2 #个人回合开始阶段
HOOK_ROUND_END   = 3 #个人回合结束阶段    Notify(HOOK_ROUND_END). 返回值为True的，则可以跳过弃牌检查的了.
HOOK_JUDGE       = 4 #判定阶段
HOOK_JUDGED      = 5 #判定结束阶段，可以修改判定的了
HOOK_DISPATCH    = 6 #摸牌，派牌阶段
HOOK_GAME        = 7 #出牌阶段
HOOK_DROP        = 8 #弃牌阶段
#--------------------------------------------------------------
#--------都是杀类攻击-------
HOOK_ATTACK   = 10  #主动攻击                  Notify(HOOK_ATTACK,AO)
HOOK_ATTACKED = 11  #被攻击                     Notify(HOOK_ATTACKED,AO)
HOOK_HURTED   = 12  #造成伤害了              Notify(HOOK_HURTED,AO,damage)
HOOK_ATTACKFAILED = 13 #攻击失败了        Notify(HOOK_ATTACKFAILED,AO)
HOOK_ATTACKOK     = 14 #攻击成功的了. Notify(HOOK_ATTACKOK,AO) 就寒冰剑可以看.

HOOK_SPELL     = 15  #法术主动攻击        Notify(HOOK_SPELL,AO)
HOOK_SPELLED   = 16  #被法术攻击了.   Notify(HOOK_SPELLED,AO)
HOOK_SPELLFAILED = 17 #法术攻击失败了. Notify(HOOK_SPELLFAILED,AO)

HOOK_SKILL     = 18  #出特殊技能的时候,主动技能.比如甘宁的黑色牌当过河拆桥.
HOOK_PANGDING  = 19  #判定牌出现了，需要通知全部玩家。（如果能篡改判定牌的话)  Notify(HOOK_PANGDING,card,player)

HOOK_LOST      = 20  #通知玩家已经遗失了一张牌 Notify(HOOK_LOST,card) #通知这个玩家，丢失一张牌.

HOOK_HEALED    = 21  #被治疗了.        Notify(HOOK_HEALED,AO,1)

TriggerMap={
		HOOK_START : 'HOOK_START',
		HOOK_ROUND_START : 'HOOK_ROUND_START',
		HOOK_ROUND_END : 'HOOK_ROUND_END',
		HOOK_JUDGE : 'HOOK_JUDGE',
		HOOK_JUDGED : 'HOOK_JUDGED',
		HOOK_DISPATCH : 'HOOK_DISPATCH',
		HOOK_GAME : 'HOOK_GAME',
		HOOK_DROP : 'HOOK_DROP',

		HOOK_ATTACK : 'HOOK_ATTACK',
		HOOK_ATTACKED : 'HOOK_ATTACKED',
		HOOK_HURTED  : 'HOOK_HURTED',
		HOOK_ATTACKFAILED: 'HOOK_ATTACKFAILED',
		HOOK_ATTACKOK : 'HOOK_ATTACKOK',
		
		HOOK_SPELL : 'HOOK_SPELL',
		HOOK_SPELLED : 'HOOK_SPELLED',
		HOOK_SPELLFAILED : 'HOOK_SPELLFAILED',

		HOOK_SKILL : 'HOOK_SKILL',
		HOOK_PANGDING : 'HOOK_PANGDING',
		
		HOOK_LOST : 'HOOK_LOST',
		
		HOOK_HEALED: 'HOOK_HEALED',
}
def getEVTName(evt): return TriggerMap.get(evt,"UNKNOWN HOOK EVT:"+str(evt))

class TriggerDB(object):
	"""
		触发器的DB部分.以便进行触发器的查找以及配合工作.
	"""
	def __init__(self):
		self.db = {}  #HOOK_SHA: [] card_obj
		self.disabled=set()  #被屏蔽的触发器
	def Hook(self,hookid,cardobj):
		"""
			安装一个钩子
			hookid:  HOOK_XXX之类的
			cardobj: 卡片对象.
		"""
		if hookid in self.db:
			self.db[hookid].append(cardobj)
		else:
			self.db[hookid] = [cardobj]
	def unHook(self,hookid,cardobj):
		"""
			卸载一个钩子
			hookid:  HOOK_SHA之类的
			cardobj: 卡片对象.
		"""
		if hookid not in self.db: return
		i = 0
		hooks = self.db[hookid]
		poslist=[]
		for t in hooks:
			if t.id == cardobj.id: poslist.append(i)
			i += 1
		poslist.reverse()
		for x in poslist: del hooks[x]
	def Disable(self,hookid):
		self.disabled.add(hookid)
	def Enable(self,hookid):
		self.disabled.remove(hookid)
	def getHook(self,hookid):
		"""
			得到一串钩子序列.
		"""
		if hookid in self.disabled: return None
		if hookid in self.db: return self.db[hookid]
		return None

if __name__=="__main__":
	pass