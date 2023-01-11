from Crypto.Cipher import DES

key = b'ExmplKey'

ptext = b'hehe hoho?'

cipher_des = DES.new(key, DES.MODE_EAX)

msg = cipher_des.nonce + cipher_des.encrypt(ptext)
print(cipher_des.nonce)
print(msg)
myNonce = msg[0:16]
print(myNonce)

myEncMsg = msg[16:len(msg)]
# print(myEncMsg)
myCipher = DES.new(key, DES.MODE_EAX, nonce=myNonce)

decryption = myCipher.decrypt(myEncMsg)



print(decryption)