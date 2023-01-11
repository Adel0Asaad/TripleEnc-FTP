from Crypto.Cipher import AES

file_in = open("AES_encrypted_data.bin", "rb")
key, nonce, tag, ciphertext = [ file_in.read(x) for x in (16, 16, 16, -1) ]
file_in.close()

#Decryption
cipher = AES.new(key, AES.MODE_EAX, nonce)
data = cipher.decrypt_and_verify(ciphertext, tag)

print(data.decode("utf-8"))