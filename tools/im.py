#coding: utf8
"""
	通知消息XMPP发送
	pip install pyxmpp2
"""
import sys,logging
try:
	from pyxmpp2.settings import XMPPSettings
	from pyxmpp2.simple import send_message
except:
	pass

class IM(object):
	def __init__(self,user,passwd,to):
		self._user = user.decode('utf8')
		self._passwd = passwd.decode('utf8')
		self._to = to.decode('utf8')
		self._settings = XMPPSettings({
			u"starttls": False,
			u"tls_verify_peer": False,
		})
	def send(self,message):
		if not message: return
		msg = message.decode('utf8')
		send_message(self._user,self._passwd,self._to,msg,settings=self._settings)

logging.basicConfig(level = logging.INFO) # change to 'DEBUG' to see more
if __name__=="__main__":
	im = IM('robot@xxxx','password','receiver@xxx')
	im.send('Come On,Baby')
