import socket
import time
import Crypto
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import ast

s = socket.socket()
host = socket.gethostname()
port = 12221
s.bind((host, port))

s.listen(5)
c = None

# -------- Criptography

# pbKeyClient1024.der
# prKeyServer1024.der
# pbKeyClient2048.der
# prKeyServer2048.der
# prKeyServer4096.der
# pbKeyClient4096.der

#get public key
f = open('pbKeyClient1024.der')
pbKeyClient = RSA.importKey(f.read())
f.close()

#get private key  
f = open('prKeyServer1024.der')
prKeyServer = RSA.importKey(f.read())
f.close()

# -------- Communication 
while True:
   if c is None:            #esperando a conexao do cliente 
       print '[Waiting for connection...]'
       c, addr = s.accept()
       print 'Got connection from', addr
   else:
       print '[Waiting for response...]'
       textocifrado = c.recv(2048)
       print 'Texto cifrado: ' + textocifrado

       #to decode, use the server's private key
       cipher = PKCS1_OAEP.new(prKeyServer)
       texto = cipher.decrypt(textocifrado)
       print 'Mensagem descriptograda: ' + texto

       q = raw_input("Enter something to this client: ")
       
       #to encode, use the client's public key 
       cipher = PKCS1_OAEP.new(pbKeyClient)
       text = cipher.encrypt(q)
       c.send(str(text))


s.close()
