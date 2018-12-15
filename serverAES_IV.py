import socket
from Crypto.Cipher import AES
from Crypto import Random
import time
import base64

s = socket.socket()
host = socket.gethostname()
port = 12221
s.bind((host, port))

# 128 bits - abcdefghijklmnop
# 192 bits - abcdefghijklmnopqrstuvwx
# 256 bits - abcdefghijklmnopqrstuvwxyz123456

bs = 16
key = 'abcdefghijklmnop'

s.listen(5)
# c = client
c = None


# -------- Criptografia
def encrypt(raw):
    raw = _pad(raw)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw))

def decrypt(enc):
    enc = base64.b64decode(enc)
    iv = enc[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return _unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

def _pad(s):
    return s + (bs - len(s) % bs) * chr(bs - len(s) % bs)

def _unpad(s):
    return s[:-ord(s[len(s)-1:])]

# -------- Comunicacao
while True:
   if c is None:
       print '[Waiting for connection...]'
       c, addr = s.accept()
       print 'Got connection from', addr 
   else:
       print '[Waiting for response...]'
       textocifrado = c.recv(16384)
       print 'Texto cifrado: ' + textocifrado
       texto = decrypt(textocifrado)
       print texto
       print 'Mensagem descriptograda: ' + texto
       q = raw_input("Enter something to this client: ")
       text = encrypt(q)
       c.send(text)



s.close()