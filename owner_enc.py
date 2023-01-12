from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import ChaCha20_Poly1305, AES, DES, PKCS1_OAEP, Salsa20

################################################ ENCRYPTIONS ################################################

def enc_ChaCha(ptext):
    key = get_random_bytes(32)

    #Encryption
    cipher = ChaCha20_Poly1305.new(key=key)
    encText = cipher.encrypt(ptext)
    return key, cipher.nonce, encText

def enc_AES(ptext):
    key = get_random_bytes(16)

    #Encryption
    cipher = AES.new(key, AES.MODE_EAX)
    encText = cipher.encrypt(ptext)
    return key, cipher.nonce, encText

def enc_DES(ptext):
    key = get_random_bytes(8)

    #Encryption
    cipher = DES.new(key, DES.MODE_EAX)
    encText = cipher.encrypt(ptext)
    return key, cipher.nonce, encText

########## MasterKey Enc ##########
def enc_Salsa(ptext):
    key = get_random_bytes(32)

    #Encryption
    cipher = Salsa20.new(key=key)
    encText = cipher.encrypt(ptext)
    return key, cipher.nonce, encText

################################################ ENCRYPTIONS ################################################

def textChop(text, i1, i2, i3, i4):
    text1 = text[i1:i2]
    text2 = text[i2:i3]
    text3 = text[i3:i4]
    return text1, text2, text3

def encrypt(plaintext):
    
    if(len(plaintext) % 3 == 1):
        cLen = len(plaintext) - 1  #Cropped length
    elif(len(plaintext) % 3 == 2):
        cLen = len(plaintext) - 2  #Cropped length
    else:
        cLen = len(plaintext)      #Cropped length
    
    chacha_start_index = 0
    chacha_end_index = cLen//3
    aes_end_index = cLen*2//3 
    des_end_index = len(plaintext)
    msg1, msg2, msg3 = textChop(plaintext, chacha_start_index, chacha_end_index, aes_end_index, des_end_index)
    
    key1, nonce1, enc1 = enc_ChaCha(msg1)
    key2, nonce2, enc2 = enc_AES(msg2)
    key3, nonce3, enc3 = enc_DES(msg3)
    
    finalKey = key1 + key2 + key3
    finalNonce = nonce1 + nonce2 + nonce3
    finalEnc = enc1 + enc2 + enc3
    finalMsg = finalNonce + finalEnc

    masterKey, masterNonce, encKey = enc_Salsa(finalKey)

    keyMsg = masterNonce + encKey

    # recepient_key = RSA.import_key(open("owner_receiver.pem").read())
    # private_key = RSA.import_key(open("owner_private.pem").read())
    # cipher_rsa = PKCS1_OAEP.new(private_key)
    # encKey = cipher_rsa.encrypt(finalKey)

    data_out = open("encrypted_data.bin", "wb")
    data_out.write(finalMsg)
    data_out.close()

    key_out = open("encrypted_key.bin", "wb")
    key_out.write(keyMsg)
    key_out.close()

    mKey_out = open("masterKey.bin", "wb")
    mKey_out.write(masterKey)
    mKey_out.close()

file_upload = open("FileToUpload.txt", "rb")
myText = file_upload.read()
file_upload.close()
encrypt(myText)