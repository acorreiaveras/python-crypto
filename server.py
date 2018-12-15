
import socket

s = socket.socket()
host = socket.gethostname()
port = 12221
s.bind((host, port))

s.listen(5)
c = None

while True:
   if c is None:
       # Halts
       print '[Waiting for connection...]'
       c, addr = s.accept()
       print 'Got connection from', addr
   else:
       # Halts
       print '[Waiting for response...]'
       resp = c.recv(16384)
       print resp
       q = raw_input("Enter something to this client: ")
       c.send(q)
