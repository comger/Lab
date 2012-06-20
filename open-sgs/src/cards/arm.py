#!/usr/bin/env python
#coding: utf8

"""
	装备
"""
from sgs.utils.uid import *

from cardkind import *
class Arm(object):
	"""
		装备类。
		存在装备和取消2种用法.
	"""
	kind = CK_ARM #装备.
	def __init__(self,name,desc=""):
		self.name = name
		self.desc = desc
		self.id   = getUID()
	def Apply(self,player,db):
		"""
			安装当使用的钩子.
			并且针对player进行操作。在装备区增加一个东西.
		"""
		pass
	def unApply(self):
		"""
			取消装备时.
			AO中的装备区也会消失一个东西.
		"""
		pass
	def Dump(self):
		print "装备:",self.name
		if self.desc: print self.desc
