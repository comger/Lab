#!/usr/bin/env python2
#coding: utf8

from distutils.core import setup

setup(
    name='sgs',
    version='0.1',
    description='open source sgs',
    author='jxppp',
	author_email='jxppp.liu@gmail.com',
    url='http://code.google.com/p/open-sgs/',
	package_dir = {'sgs': 'src'},
	packages = [
		'sgs',
		'sgs.aos',
		'sgs.cards',
		'sgs.cards.base',
		'sgs.cards.arms',
		'sgs.cards.horses',
		'sgs.cards.npcs',
		'sgs.cards.spells',
		'sgs.cards.weapons',
		'sgs.emulator',
		'sgs.messages',
		'sgs.net',
		'sgs.players',
		'sgs.resource',
		'sgs.room',
		'sgs.test',
		'sgs.triggers',
		'sgs.utils'],
)
