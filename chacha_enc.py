from Crypto.Random import get_random_bytes
from Crypto.Cipher import ChaCha20_Poly1305

plaintext = "Well well well, look who we have here, if it isn\'t the famous James Bond himself!".encode("utf-8")
file_out = open("ChaCha_encrypted_data.bin", "wb")
key = get_random_bytes(32)

#Encryption
cipher_chacha = ChaCha20_Poly1305.new(key=key)

encText, tag = cipher_chacha.encrypt_and_digest(plaintext)

[ file_out.write(x) for x in (key, cipher_chacha.nonce, tag, encText) ]