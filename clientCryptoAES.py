import socket
from Crypto.Cipher import AES
from Crypto import Random
import time

s = socket.socket()
host = '192.168.0.21'
port = 12221

# 128 bits - abcdefghijklmnop
# 192 bits - abcdefghijklmnopqrstuvwx
# 256 bits - abcdefghijklmnopqrstuvwxyz123456

key = b'abcdefghijklmnop'
# cipher = AES.new(key)
iv = Random.new().read(AES.block_size)
cipher = AES.new(key, AES.MODE_CBC, iv)

s.connect((host, port))
print 'Connected to', host

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
    z = raw_input("Enter something for the server: ")

    start = time.time()
    # retirar iv
    text = iv + encrypt(z)
    tempEncrip = time.time() - start
    print 'Tempo de Encriptacao: ', tempEncrip

    s.send(text)
    print '[Waiting for response...]'
    textocifrado = s.recv(2048)
    print 'Texto cifrado: ' + textocifrado

    startd = time.time()
    texto = decrypt(textocifrado)
    tempDecrip = time.time() - startd

    print 'Mensagem descriptograda: ' + texto
    print 'Tempo de Decriptacao: ', tempDecrip



s.close()