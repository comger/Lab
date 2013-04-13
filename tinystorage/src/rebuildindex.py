#!/usr/bin/env python2
#coding: utf8

from storage import textStorage
from indexer import sqliteIndexer,leveldbIndexer

def rebuild(indexfile,datafile):
	"""
		根据Storage文件，重新构建索引。
	"""
#	indexerobj = sqliteIndexer(indexfile)
	indexerobj = leveldbIndexer(indexfile)

	storageobj = textStorage(datafile)
	storageobj.start()
	storageobj.rescan(indexerobj.rebuild)
	
if __name__=="__main__":
	import sys
	if len(sys.argv) != 3:
		print "Usage:",sys.argv[0]," IndexFile DataFile"
		sys.exit(0)
	rebuild(sys.argv[1],sys.argv[2])
