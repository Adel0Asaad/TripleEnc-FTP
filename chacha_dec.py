from Crypto.Cipher import ChaCha20_Poly1305

file_in = open("ChaCha_encrypted_data.bin", "rb")


key, nonce, tag, ciphertext = \
   [ file_in.read(x) for x in (32, 12, 16, -1) ]
file_in.close()

#Decryption
try:
    cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
    decr = cipher.decrypt_and_verify(ciphertext, tag)
    print(decr.decode("utf-8"))
except (ValueError, KeyError):
    print("Incorrect decryption")