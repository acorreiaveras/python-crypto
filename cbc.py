import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
import time

bs = 24
key = 'abcdefghijklmnopqrstuvwx'
message = 'oi'

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



start = time.time()
text = encrypt(message)
tempEncrip = time.time() - start


startd = time.time()
texto = decrypt(message)
tempDecrip = time.time() - startd

print 'Tempo de Encriptacao: ', tempEncrip
print 'Tempo de Decriptacao: ', tempDecrip
