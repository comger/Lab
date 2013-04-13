#coding: utf8
"""
	完全是数据的保存状态
	数据只保留2部分

	key  ->  用户可以自定义的唯一标示这条数据的内容
	size status time-> 数据文件的大小，状态(status: 1:合法的,0:删除),操作的时间(豪秒值now())
	data[size]
"""
import os,os.path
import sqlite3
import leveldb

class leveldbIndexer(object):
	"""
		基于SQLite的索引器部分
	"""
	def __init__(self,dbdir):
		self._conn = leveldb.LevelDB(dbdir)
	def read(self,key):
		"""
			返回offset的位置
		"""
		try:
			return int(self._conn.Get(key))
		except:
			return -1
	def write(self,key,offset):
		self._conn.Put(key,str(offset))
	def delete(self,key):
		self._conn.Delete(key)
	def rebuild(self,key,ct,offset):
		#被将会被Storage调用的
		self._conn.Put(key,str(offset))

class sqliteIndexer(object):
	"""
		基于SQLite的索引器部分
	"""
	def __init__(self,indexfile):
		"""
			indexfile: 索引SQlite文件
		"""
		if not os.path.exists(indexfile):
			self._conn = sqlite3.connect(indexfile)
			c = self._conn.cursor()
			c.execute('CREATE TABLE KVS(K text PRIMARY KEY,OFFSET int)')
			self._conn.commit()
			c.close()
		else:
			self._conn = sqlite3.connect(indexfile)

		self._cursor = self._conn.cursor()
		self._cursor.execute('PRAGMA synchronous=OFF')

	def read(self,key):
		"""
			返回offset的位置
		"""
		self._cursor.execute('SELECT OFFSET FROM KVS WHERE K=?',(key.decode('utf8'),))
		offset = -1
		for off, in self._cursor.fetchall():
			offset = off

		if not offset or offset < 0:
			return -1

		return offset
	def write(self,key,offset):
		#当前是否已经存在?
		self._cursor.execute('INSERT OR REPLACE INTO KVS VALUES(?,?)',(key,offset))
		self._conn.commit()
	def delete(self,key):
		self._cursor.execute('DELETE FROM KVS WHERE K=?',(key,))
		self._conn.commit()
	def rebuild(self,key,ct,offset):
		#被将会被Storage调用的
		self._cursor.execute('INSERT OR REPLACE INTO KVS VALUES(?,?)',(key,offset))
		self._conn.commit()

if __name__=="__main__":
	i = sqliteIndexer('1.sqlite3')
	from basetools import now
	a= now()
	for x in xrange(200000):
		i.write("%s"%x)
	print now()-a
