# generate keys for client
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random

# -------- Criptography
#random_generator = Random.new().read
#key = RSA.generate(1024, random_generator) #generate pub and priv key

# 1024b
# 2048b
# 4096b

key = RSA.generate(4096)

#export public key
print(key.publickey().exportKey())

f = open('pbKeyClient4096.der','w')
f.write(key.publickey().exportKey('DER'))
f.close()

#export private key 
print(key.exportKey())

f = open('prKeyClient4096.der','w')
f.write(key.exportKey('DER'))
f.close()

