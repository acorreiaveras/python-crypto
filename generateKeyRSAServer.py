# generate keys for server
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random

# -------- Criptografia
#random_generator = Random.new().read
#key = RSA.generate(1024, random_generator) #generate pub and priv key

# 1024b
# 2048b
# 4096b

key = RSA.generate(4096)

#exportar chave publica
print(key.publickey().exportKey())

f = open('pbKeyServer4096.der','w')
f.write(key.publickey().exportKey('DER'))
f.close()

#exportar chave privada 
print(key.exportKey())

f = open('prKeyServer4096.der','w')
f.write(key.exportKey('DER'))
f.close()