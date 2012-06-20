#!/usr/bin/env python
#coding: utf8


"""
	卡的种类
"""
#----基础类------
CK_SHA  = 10000000  #杀
CK_SHAN = 10000001  #闪
CK_TAO  = 10000002  #桃
#----法术类------
CK_SPELL        = 11000000     #法术类
CK_WXKJ         = 11000001     #无懈可击
CK_GHCQ         = 11000002     #过河拆桥
CK_WJQF         = 11000003     #万箭齐发
CK_WZSY         = 11000004     #无中生有
CK_SSQY         = 11000005     #顺手牵羊
CK_JUEDOU       = 11000006     #决斗
CK_NMRQ         = 11000007     #南蛮入侵
CK_TYJY         = 11000008     #桃园结义
CK_WGFD         = 11000009     #五谷丰登
CK_LBSS         = 11000010     #乐不思蜀
CK_SD           = 11000011     #闪电
CK_JDSR         = 12000012     #借刀杀人

def isSpellCard(card):         #是不是法术牌
	kind = card.ObjKind()
	return kind >= CK_SPELL and kind < CK_ARM
#----防局类-------
CK_ARM          = 12000000   #
CK_BGZ          = 12000001   #八卦阵
CK_RWD          = 12000002   #仁王盾

def isArmCard(card):
	kind = card.ObjKind()
	return (kind >= CK_ARM) and (kind < CK_WEAPON)
#-----武器类---------
CK_WEAPON       = 13000000
CK_QLYYD        = 13000000  #青龙偃月刀
CK_ZGLN         = 13000001  #诸葛连弩
CK_HBJ          = 13000002  #寒冰剑.
CK_QGJ          = 13000003  #青釭剑.
CK_GSF          = 13000004  #贯石斧

def isWeaponCard(card):
	kind = card.ObjKind()
	return (kind >= CK_WEAPON) and (kind < CK_ADDMA)
#-----加马------------
CK_ADDMA        = 14000000  #加马
CK_JY           = 14000001  #绝影

def isAddMaCard(card):
	kind = card.ObjKind()
	return (kind >= CK_ADDMA) and (kind < CK_DECMA)
#-----减马------------
CK_DECMA        = 15000000  #减马
def isDecMaCard(card):
	kind = card.ObjKind()
	return (kind >= CK_DECMA) and (kind < CK_NPC)
#----武将类---------
CK_NPC          = 19000000

#---效果类----------
CK_EFFECT       = 20000000
CK_EFF_XUE      = 20000001 #血效果,加减都可以
CK_EFF_SHEN     = 20000002 #神效果
