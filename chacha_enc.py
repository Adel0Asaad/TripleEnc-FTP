import json
from base64 import b64encode, b64decode
from Crypto.Random import get_random_bytes
from Crypto.Cipher import ChaCha20_Poly1305

header = b'header'
key = get_random_bytes(32)
plaintext = "Well well well, look who we have here, if it isn\'t the famous James Bond himself!".encode("utf-8")
cipher_chacha = ChaCha20_Poly1305.new(key=key)
cipher_chacha.update(header)

encText, tag = cipher_chacha.encrypt_and_digest(plaintext)

jk = [ 'nonce', 'header', 'ciphertext', 'tag' ]
jv = [ b64encode(x).decode('utf-8') for x in (cipher_chacha.nonce, header, encText, tag) ]
result = json.dumps(dict(zip(jk, jv)))
print(result)

try:
    b64 = json.loads(result)
    jk = [ 'nonce', 'header', 'ciphertext', 'tag' ]
    jv = {k:b64decode(b64[k]) for k in jk}
    cipher = ChaCha20_Poly1305.new(key=key, nonce=jv['nonce'])
    cipher.update(jv['header'])
    aaaaaaa = cipher.decrypt_and_verify(jv['ciphertext'], jv['tag'])
    print("The message was: ")
    print(aaaaaaa)
except (ValueError, KeyError):
    print("Incorrect decryption")