#!/usr/bin/env python
#coding: utf8


class Base(object):
	def __init__(self,obj):
		self.obj = obj
	def Apply(self,*sth):
		print "in Base:Apply"
		self.obj.Apply(*sth)
	
class A(object):
	def Apply(self,a):
		print "In A:Apply",a

class B(object):
	def Apply(self,a,b):
		print "In B:Apply:",a,b
		
		
if __name__=="__main__":
	
	a = Base(A())
	b = Base(B())

	a.Apply("a")
	b.Apply("a","b")