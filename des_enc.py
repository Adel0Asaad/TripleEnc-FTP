from Crypto.Random import get_random_bytes
from Crypto.Cipher import DES


ptext = "I\'m testing to see how far I can take the plaintext to, because it said to only input 64 bytes :(".encode("utf-8")
file_out = open("DES_encrypted_data.bin", "wb")


key = get_random_bytes(8)

#Encryption
cipher_des = DES.new(key, DES.MODE_EAX)
ciphertext = cipher_des.encrypt(ptext)

[ file_out.write(x) for x in (key, cipher_des.nonce, ciphertext)]
file_out.close()