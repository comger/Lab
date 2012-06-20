#!/usr/bin/env python
#coding: utf8

ROLE_ZG   = 1   #主公角色
ROLE_ZC   = 2   #忠臣角色
ROLE_NJ   = 3   #内奸
ROLE_FZ   = 4   #反贼

def RoleName(role):
	ROLE_MAP={
		ROLE_ZG : '主公',
		ROLE_ZC : '忠臣',
		ROLE_NJ : '内奸',
		ROLE_FZ : '反贼'
	}
	return ROLE_MAP.get(role)