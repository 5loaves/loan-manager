from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer

class SimpleChat(WebSocket):

   def handleMessage(self):
      if self.data is None:
         self.data = ''
      
      for client in self.server.connections.itervalues():
         if client != self:
            try:
               client.sendMessage(str(self.data))
            except Exception as n:
               print n


   def handleConnected(self):
      print self.address, 'connected'
      for client in self.server.connections.itervalues():
         if client != self:
            try:
               client.sendMessage('connected')
            except Exception as n:
               print n

   def handleClose(self):
      print self.address, 'closed'
      for client in self.server.connections.itervalues():
         if client != self:
            try:
               client.sendMessage('disconnected')
            except Exception as n:
               print n

server = SimpleWebSocketServer('', 5522, SimpleChat)
server.serveforever()
