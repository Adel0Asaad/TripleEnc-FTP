from Crypto.Random import get_random_bytes
from Crypto.Cipher import DES

file_in = open("DES_encrypted_data.bin", "rb")



key, nonce, ciphertext = \
    [ file_in.read(x) for x in (8, 16, -1)]
file_in.close()

#Decryption
cipher_des = DES.new(key, DES.MODE_EAX)

myCipher = DES.new(key, DES.MODE_EAX, nonce=nonce)

decryption = myCipher.decrypt(ciphertext)

print(decryption.decode("utf-8"))