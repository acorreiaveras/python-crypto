import socket
from Crypto.Cipher import AES
from Crypto import Random
import time
import base64

s = socket.socket()
host = '192.168.0.8'
port = 12221

# 16B - abcdefghijklmnop
# 24B - abcdefghijklmnopqrstuvwx
# 32B - abcdefghijklmnopqrstuvwxyz123456

bs = 16
key = 'abcdefghijklmnop'

s.connect((host, port))
print 'Connected to', host

ctrl = True
i = 0


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
while ctrl:
    if(i == 2):
        ctrl = False
    else:

        z = raw_input("Enter something for the server: ")

        start = time.time()
        text = encrypt(z)
        tempEncrip = time.time() - start
        print 'Tempo de Encriptacao: ', tempEncrip
        texto = decrypt(text)
        print texto

        s.send(text)
        print '[Waiting for response...]'
        textocifrado = s.recv(16384)
        print 'Texto cifrado: ' + textocifrado

        startd = time.time()
        texto = decrypt(textocifrado)
        tempDecrip = time.time() - startd

        print 'Mensagem descriptograda: ' + texto
        print 'Tempo de Decriptacao: ', tempDecrip

        i = i + 1

s.close()
