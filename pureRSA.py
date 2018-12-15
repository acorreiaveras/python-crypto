import time
import Crypto
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def enc(message, pubKey, prvKey):
    #get public key
    f = open(pubKey)
    pbKeyClient = RSA.importKey(f.read())
    f.close()

    # get private key  
    f = open(prvKey)
    prKeyClient = RSA.importKey(f.read())
    f.close()
    
    for i in range(0,32):
        start = time.time()    
        cipher = PKCS1_OAEP.new(pbKeyClient)
        text = cipher.encrypt(message)
        tempEncrip = time.time() - start

        startd = time.time()
        cipher = PKCS1_OAEP.new(prKeyClient)
        texto = cipher.decrypt(text)
        tempDecrip = time.time() - startd

        print 'Tempo de Encriptacao: ', tempEncrip
        print 'Tempo de Decriptacao: ', tempDecrip
    print ''

message1 = 'Lorem ipsum congue nisi sem tincidunt dictum, justo mattis primis enim tempus ultrices'
message2 = 'Lorem ipsum congue nisi sem tincidunt dictum, justo mattis primis enim tempus ultrices nunc, fermentum dui viverra lacus etiam. feugiat facilisis vitae conubia amet pretium sagittis conubia nulla, accumsan donec nu'
message3 = 'Lorem ipsum congue nisi sem tincidunt dictum, justo mattis primis enim tempus ultrices nunc, fermentum dui viverra lacus etiam. feugiat facilisis vitae conubia amet pretium sagittis conubia nulla, accumsan donec nullam venenatis faucibus leo pharetra et hendrerit, porta placerat lacinia sollicitudin tempus eros habitasse. mauris dictum lorem hendrerit non hendrerit ipsum posuere, aenean ac semper scelerisque dapibus dictum cubilia, proin enim ac aenean curae nisias.'

enc(message1, 'pbKeyClient1024.der', 'prKeyClient1024.der')
enc(message1, 'pbKeyClient2048.der', 'prKeyClient2048.der')
enc(message1, 'pbKeyClient4096.der', 'prKeyClient4096.der')




