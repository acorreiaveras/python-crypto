'''

1. Receive encrypted message 
2. Decrypt AES's key using the RSA algorithm
3. Save it on a file (.der/.pem)
4. Initiate communication using the AES received key

'''
import socket
import Crypto
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto import Random
from Crypto.Cipher import AES
import time
import base64

lastMessage = ''

bs = 32 #chave de 32bits

# -------- Socket
s = socket.socket()
host = '192.168.0.8'
port = 12221

s.connect((host, port))
print 'Connected to', host

# -------- Criptografia
def encrypt(raw):
    raw = _pad(raw)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(keyAES, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw))

def decrypt(enc):
    enc = base64.b64decode(enc)
    iv = enc[:AES.block_size]
    cipher = AES.new(keyAES, AES.MODE_CBC, iv)
    return _unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

def _pad(s):
    return s + (bs - len(s) % bs) * chr(bs - len(s) % bs)

def _unpad(s):
    return s[:-ord(s[len(s)-1:])]

#get public key
f = open('pbKeyServer2048.der')
pbKeyServer = RSA.importKey(f.read())
f.close()

#get private key  
f = open('prKeyClient2048.der')
prKeyClient = RSA.importKey(f.read())
f.close()

i=0
ctr = True

# -------- Comunicacao
while ctr:

    startd = time.time()
    textocifrado = s.recv(1024)
    cipherRSA = PKCS1_OAEP.new(prKeyClient)
    keyAES = cipherRSA.decrypt(textocifrado)
    cipher = AES.new(keyAES)
    s.send('OK')
        
    text = s.recv(2048)
    texto = decrypt(text)
    tempDecrip = time.time() - startd
    print tempDecrip

    i=i+1

    if(i == 10): 
        ctr = False

s.close()