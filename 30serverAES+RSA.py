'''

1. Generate RSA's keys use the generator
2. Encrypt AES's key using the RSA key 
3. Send to the Client the encrypted message
4. Initiate communication

'''
import socket
import Crypto
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto import Random
from Crypto.Cipher import AES
import base64

bs = 32 #chave de 32bits

lastMessage = '' # control the key sending
AESKey = 'abcdefghijklmnopqrstuvwxyz123456'
textToSend = 'Oi'

# -------- Socket
s = socket.socket()
host = socket.gethostname()
port = 12221
s.bind((host, port))
s.listen(5)
client = None

# -------- Criptografia
def encrypt(raw):
    raw = _pad(raw)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(AESKey, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw))

def decrypt(enc):
    enc = base64.b64decode(enc)
    iv = enc[:AES.block_size]
    cipher = AES.new(AESKey, AES.MODE_CBC, iv)
    return _unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

def _pad(s):
    return s + (bs - len(s) % bs) * chr(bs - len(s) % bs)

def _unpad(s):
    return s[:-ord(s[len(s)-1:])]

#get public key
f = open('pbKeyClient2048.der')
pbKeyClient = RSA.importKey(f.read())
f.close()

#get private key  
f = open('prKeyServer2048.der')
prKeyServer = RSA.importKey(f.read())
f.close()

i=0
ctr = True
 
# -------- Comunicacao
while ctr:
    if client is None:
        print '[Waiting for connection...]'
        client, addr = s.accept()
        print 'Got connection from', addr
    else:

        cipherRSA = PKCS1_OAEP.new(pbKeyClient)
        text = cipherRSA.encrypt(AESKey)
        client.send(text)
        test = client.recv(2048)       

        text = encrypt('Hi client, this is my first message')
        client.send(text)

        i=i+1

        if(i == 32): 
            ctr = False



s.close()


