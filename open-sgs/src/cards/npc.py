#!/usr/bin/env python
#coding: utf8

from sgs.utils.uid import *
from cardkind import *

MALE = 0       #男
FEMALE = 1     #女

class NPC(object):
	"""
		武将系列.
		触发条件.
	"""
	kind = CK_NPC
	def __init__(self,name,life,sex,desc=""):
		"""
			name: 武将名称
			life: 武将的气血
			sex :  性别
			desc: 武将的描述
		"""
		self.id = getUID()
		self.maxlife = life
		self.life = life
		self.name = name
		self.desc = desc
		self.sex  = sex
		
		self.usekill = 1       #用杀的次数.每个回合只能是一次的，除非特殊技能.
		self.dodge_range  = 0  #躲避距离
		self.attack_range = 1  #攻击距离
	def Apply(self,db):
		"""
			特殊技能的安装.
			在npc被选定后，就应该自动的调用.
		"""
		pass
	def Dump(self):
		print "姓名:",self.name
		if self.sex == MALE: print "性别:","男"
		else: print "性别:","女"
		print "最大气血:",self.maxlife
		print "当前气血:",self.life
		print "杀可用次数:",self.usekill
		print "躲避距离:",self.dodge_range
		print "攻击距离:",self.attack_range
		if self.desc: print self.desc
