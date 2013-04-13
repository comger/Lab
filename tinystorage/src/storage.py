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

from basetools import now
class textStorage(object):
	"""
		存储为单个文件
	"""
	def __init__(self,fn):
		self.name = fn
		self.fd = None
	def start(self):
		"""
			开始加载这个数据文件.
		"""
		if self.fd: self.fd.close()
		self.fd = open(self.name,"a+") #打开这个文件
		return True
	def rescan(self,cb):
		"""
			重新扫描这个文件
			后续希望重建索引，或者重新压缩掉已经删除的Key都是可行的了
			cb -> func(key,ct,offset)
			key  ->  用户可以自定义的唯一标示这条数据的内容
			size status time-> 数据文件的大小，状态(status: 1:合法的,0:删除),操作的时间(豪秒值now())
			data[size]
		"""
		if not cb: return

		filesize = os.stat(self.name).st_size
		if not self.fd:
			self.fd = open(self.name)

		existed ={} #key: (ct,offset) 有效的Key，只保留最后一个ct时间的数据.
		deleted ={} #key: (ct,offset) #后面好删除用，也只保留最后一次删除的
		offset = 0
		self.fd.seek(0,os.SEEK_SET) #回到头部
		while offset < filesize:
			key = self.fd.readline().strip()
			size,status,ct = map(int,self.fd.readline().strip().split())

			n = (ct,offset)
			if status == 0:
				if (key not in deleted) or (n > deleted[key]):
					deleted[key] = n
			elif status == 1: #合法的
				#需要比较ct的大小，只保留最后一个.
				if (key not in existed) or (n > existed[key]):
					existed[key] = n
			else:
				raise Exception("未知的状态[%s]@Offset:%s" % (status,offset))
			self.fd.seek(size,os.SEEK_CUR) #跳过数据内容
			offset = self.fd.tell()
		#在deleted中删除existed
		for key,d in deleted.iteritems():
			if key not in existed: continue
			e = existed[key]
			if d > e:
				del existed[key] #删除这个

		for key,n in existed.iteritems():
			cb(key,n[0],n[1])
	def read(self,key,offset):
		"""
			读取某个Key的数据.
			key  ->  用户可以自定义的唯一标示这条数据的内容
			size status time-> 数据文件的大小，状态(status: 1:合法的,0:删除),操作的时间(豪秒值now())
			data[size]
		"""
		self.fd.seek(offset,os.SEEK_SET)
		if self.fd.readline().strip() != key:
			raise Exception("Storage %s read %s Key[%s] Error" % (self.name,offset,key))

		size,status,ct = map(int,self.fd.readline().strip().split())
		if status == 0:
			raise Exception("Storage %s read %s Key[%s] Deleted" % (self.name,offset,key))
		return self.fd.read(size) #返回数据
	def delete(self,key):
		"""删除某个数据"""
		self.fd.seek(0,os.SEEK_END)
		key ='%s' % key
		self.fd.write('%s\n0 0 %s\n' % (key.strip(),now()))
		self.fd.flush()
	def write(self,key,data):
		""" 返回写入的初始地址 """
		self.fd.seek(0,os.SEEK_END)
		offset = self.fd.tell() #当前的偏移位置
		key ='%s' % key
		self.fd.write('%s\n%s 1 %s\n' % (key.strip(),len(data),now()))
		self.fd.write(data)
		self.fd.flush()
		return offset

if __name__=="__main__":
	pass
