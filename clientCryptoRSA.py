import socket
import time
import Crypto
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

s = socket.socket()
#host = '192.168.100.14'
host = socket.gethostname()
port = 12221

s.connect((host, port))
print 'Connected to', host


# -------- Criptography

# pbKeyServer1024.der
# prKeyClient1024.der
# pbKeyServer2048.der
# prKeyClient2048.der
# pbKeyServer4096.der
# prKeyClient4096.der

#get public key
f = open('pbKeyServer1024.der')
pbKeyServer = RSA.importKey(f.read())
f.close()

#get private key  
f = open('prKeyClient1024.der')
prKeyClient = RSA.importKey(f.read())
f.close()

# -------- Communication 
while True:  

    z = raw_input("Enter something for the server: ")
   
    #to encode, use the client's public key
    start = time.time()    
    cipher = PKCS1_OAEP.new(pbKeyServer)
    text = cipher.encrypt(z)
    tempEncrip = time.time() - start
    print 'Tempo de Encriptacao: ', tempEncrip

    s.send(str(text))
    
    print '[Waiting for response...]'
    textocifrado = s.recv(2048)
    print 'Texto cifrado: ' + textocifrado
    
    #to decode, use the client's private key
    startd = time.time()
    cipher = PKCS1_OAEP.new(prKeyClient)
    texto = cipher.decrypt(textocifrado)
    tempDecrip = time.time() - startd

    print 'Mensagem descriptograda: ' + texto
    print 'Tempo de Decriptacao: ', tempDecrip
    
s.close()


