from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

data = "secret data".encode("utf-8")

key = get_random_bytes(16)
cipher = AES.new(key, AES.MODE_EAX)
ciphertext, tag = cipher.encrypt_and_digest(data)

file_out = open("AES_encrypted_data.bin", "wb")
[ file_out.write(x) for x in (key, cipher.nonce, tag, ciphertext) ]
file_out.close()