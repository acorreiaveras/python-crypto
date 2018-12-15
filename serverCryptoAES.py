import socket
from Crypto.Cipher import AES
from Crypto import Random
import time

s = socket.socket()
host = socket.gethostname()
port = 12221
s.bind((host, port))

# 128 bits - abcdefghijklmnop
# 192 bits - abcdefghijklmnopqrstuvwx
# 256 bits - abcdefghijklmnopqrstuvwxyz123456

key = b'abcdefghijklmnop'
iv = Random.new().read(AES.block_size)
cipher = AES.new(key, AES.MODE_CBC, iv)


s.listen(5)
# c = client
c = None

# -------- Criptografia
def pad(s):
    return s + ((16-len(s) % 16) * '{')

def encrypt(plaintext):
    global cipher
    return cipher.encrypt(pad(plaintext))

def decrypt(ciphertext):
    global cipher
    dec = cipher.decrypt(ciphertext)
    l = dec.count('{')
    return dec[:len(dec)-l]

# -------- Comunicacao
while True:
   if c is None:
       print '[Waiting for connection...]'
       c, addr = s.accept()
       print 'Got connection from', addr
   else:
       print '[Waiting for response...]'
       textocifrado = c.recv(2048)
       print 'Texto cifrado: ' + textocifrado
       texto = decrypt(textocifrado)
       print 'Mensagem descriptograda: ' + texto
       q = raw_input("Enter something to this client: ")
       # retirar iv 
       text = iv + encrypt(q)
       c.send(text)



s.close()