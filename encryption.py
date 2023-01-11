from Crypto.Random import get_random_bytes
from Crypto.Cipher import ChaCha20_Poly1305, AES, DES

def enc_ChaCha(ptext):
    ptext = ptext.encode("utf-8")
    key = get_random_bytes(32)

    #Encryption
    cipher = ChaCha20_Poly1305.new(key=key)
    encText = cipher.encrypt(ptext)
    return key, cipher.nonce, encText

def enc_AES(ptext):
    ptext = ptext.encode("utf-8")
    key = get_random_bytes(16)

    #Encryption
    cipher = AES.new(key, AES.MODE_EAX)
    encText = cipher.encrypt(ptext)
    return key, cipher.nonce, encText

def enc_DES(ptext):
    ptext = ptext.encode("utf-8")
    key = get_random_bytes(8)

    #Encryption
    cipher = DES.new(key, DES.MODE_EAX)
    encText = cipher.encrypt(ptext)
    return key, cipher.nonce, encText

    

def textChop(text, i1, i2, i3, i4):
    print(text, i1, i2, i3, i4)
    text1 = text[i1:i2]
    text2 = text[i2:i3]
    text3 = text[i3:i4]
    return text1, text2, text3

def encrypt(plaintext):
    if(len(plaintext) % 3 == 1):
        print("1, " + str(len(plaintext)))
        cLen = len(plaintext) - 1 #Cropped length
        chacha_start_index = 0
        chacha_end_index = cLen//3
        aes_end_index = cLen*2//3 
        des_end_index = len(plaintext)
        msg1, msg2, msg3 = textChop(plaintext, chacha_start_index, chacha_end_index, aes_end_index, des_end_index)
    elif(len(plaintext) % 3 == 2):
        print("2, " + str(len(plaintext)))
        cLen = len(plaintext) - 2 #Cropped length
        chacha_start_index = 0
        chacha_end_index = cLen//3
        aes_end_index = cLen*2//3 
        des_end_index = len(plaintext)
        msg1, msg2, msg3 = textChop(plaintext, chacha_start_index, chacha_end_index, aes_end_index, des_end_index)
    else:
        print("0, " + str(len(plaintext)))
        chacha_start_index = 0
        chacha_end_index = len(plaintext)//3
        aes_end_index = len(plaintext)*2//3
        des_end_index = len(plaintext)
        msg1, msg2, msg3 = textChop(plaintext, chacha_start_index, chacha_end_index, aes_end_index, des_end_index)

    print(msg1, msg2, msg3)
    key1, nonce1, enc1 = enc_ChaCha(msg1)
    key2, nonce2, enc2 = enc_AES(msg2)
    key3, nonce3, enc3 = enc_DES(msg3)
    print(enc1, enc2, enc3)
    finalKey = key1 + key2 + key3
    finalEnc = enc1 + enc2 + enc3
    print(finalEnc)

myText = "Hello"
encrypt(myText)