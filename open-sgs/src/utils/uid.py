#!/usr/bin/env python
#coding: utf8


LOCAL_UID = 1

def getUID():
	"""
		得到一个唯一的ID号.
	"""
	global LOCAL_UID
	id = LOCAL_UID
	LOCAL_UID +=1
	return id