import IrcConnection
import MessageHandler


class IrcBot:
	def __init__(self):
		self._connections 		= list()
		self._messageHandlers	= list()
		self._run 				= False
		
	def addConnection(self, con):
		self._connections.append(con)
	
	def addMessageHandler(self, handler):
		self._messageHandlers.append(handler)
	
	def run(self):
		self._run = True
		for con in self._connections:
			con.start()
		try:
			while self._run:
				for con in self._connections:
					data = con.getData()
					if data:
						for handler in self._messageHandlers:
							handler.update(data)
							replyMessage = handler.getMessage()
							if replyMessage:
								print('Sent message: ' + replyMessage[0] + ' ' + replyMessage[1])
								con.sendMessage(replyMessage[0] + ' ' + replyMessage[1])
			
			for con in self._connections:
				con.join()
		except KeyboardInterrupt:
				for con in self._connections:
					con.logout()
				self._run = False
				for con in self._connections:
					con.join()
