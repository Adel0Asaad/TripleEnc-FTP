from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import ChaCha20_Poly1305, AES, DES, PKCS1_OAEP

def dec_ChaCha(key, nonce, ctext):

    cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
    ptext = cipher.decrypt(ctext)
    return ptext

def dec_AES(key, nonce, ctext):

    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    ptext = cipher.decrypt(ctext)
    return ptext


def dec_DES(key, nonce, ctext):

    cipher = DES.new(key, DES.MODE_EAX, nonce=nonce)
    ptext = cipher.decrypt(ctext)
    return ptext


    

def textChop(text, i1, i2, i3, i4):
    text1 = text[i1:i2]
    text2 = text[i2:i3]
    text3 = text[i3:i4]
    return text1, text2, text3

def decrypt():
    data_in = open("encrypted_data.bin", "rb")
    nonce1, nonce2, nonce3, allEnc = \
        [ data_in.read(x) for x in (12, 16, 16, -1) ]
    data_in.close()
    
    privateKey = RSA.import_key(open("private.pem").read())
    key_in = open("encrypted_key.bin", "rb")
    encKey = key_in.read()
    key_in.close()
    
    cipher_rsa = PKCS1_OAEP.new(privateKey)
    finalKey = cipher_rsa.decrypt(encKey)
    key1, key2, key3 = \
        [ finalKey[x:y] for x,y in ((0, 32), (32, 48), (48, 56)) ]

    if(len(allEnc) % 3 == 1):
        cLen = len(allEnc) - 1  #Cropped length
    elif(len(allEnc) % 3 == 2):
        cLen = len(allEnc) - 2  #Cropped length
    else:
        cLen = len(allEnc)      #Cropped length
    
    chacha_start_index = 0
    chacha_end_index = cLen//3
    aes_end_index = cLen*2//3 
    des_end_index = len(allEnc)
    enc1, enc2, enc3 = textChop(allEnc, chacha_start_index, chacha_end_index, aes_end_index, des_end_index)
    
    msg1 = dec_ChaCha(key1, nonce1, enc1)
    msg2 = dec_AES(key2, nonce2, enc2)
    msg3 = dec_DES(key3, nonce3, enc3)

    print((msg1+msg2+msg3).decode("utf-8"))

decrypt()