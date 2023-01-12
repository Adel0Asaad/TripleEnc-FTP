# file is created
# owner encrypts
# owner stores masterkey
# owner file uploads to FTP
# user downloads file from FTP
# user requests masterkey from owner (NOT DONE YET)
# owner encrypts masterkey with owner_private_key, and then user_public_key
# owner sends masterkey 
# user receives masterkey
# user decrypts masterkey with user_private_key, and then owner_public_key
# user has masterkey -> can decrypt file
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, Salsa20, ChaCha20_Poly1305, AES, DES

def ownerSendMKey():

    key_in = open("masterKey.bin", "rb")
    finalKey =  key_in.read()
    key_in.close()

    recepient_key = RSA.import_key(open("user_receiver.pem").read())
    # private_key = RSA.import_key(open("owner_private.pem").read())
    # cipher_rsa_owner_private = PKCS1_OAEP.new(private_key)
    cipher_rsa_user_public = PKCS1_OAEP.new(recepient_key)
    
    print(finalKey)
    # encKeys1 = cipher_rsa_owner_private.encrypt(finalKey)
    encKey = cipher_rsa_user_public.encrypt(finalKey)
    

    key_out = open("pp_mKey.bin", "wb")
    key_out.write(encKey)
    key_out.close()

def userReceiveMKey():

    key_in = open("pp_mKey.bin", "rb")
    finalKey =  key_in.read()
    key_in.close()

    # recepient_key = RSA.import_key(open("owner_receiver.pem").read())
    private_key = RSA.import_key(open("user_private.pem").read())
    cipher_rsa_user_private = PKCS1_OAEP.new(private_key)
    # cipher_rsa_owner_public = PKCS1_OAEP.new(recepient_key)
    # encKeys1 = cipher_rsa_owner_public.decrypt(finalKey)
    mKey = cipher_rsa_user_private.decrypt(finalKey)
    
    return mKey

def userDecKeys(masterKey):

    keys_in = open("encrypted_key.bin", "rb")
    masterNonce, encKey = \
        [ keys_in.read(x) for x in (8, -1) ]
    keys_in.close()
    master_cipher = Salsa20.new(key=masterKey, nonce=masterNonce)
    allKeys = master_cipher.decrypt(encKey)

    return allKeys


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


    

def textChop(keys, text, i1, i2, i3, i4):

    enc1, enc2, enc3 = \
        [ text[x:y] for x,y in ((i1, i2),(i2, i3),(i3, i4)) ]
    
    key1, key2, key3 = \
        [ keys[x:y] for x,y in ((0, 32), (32, 48), (48, 56)) ]

    return key1, key2, key3, enc1, enc2, enc3

def decrypt(allKeys):
    data_in = open("encrypted_data.bin", "rb")
    nonce1, nonce2, nonce3, allEnc = \
        [ data_in.read(x) for x in (12, 16, 16, -1) ]
    data_in.close()

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

    key1, key2, key3, enc1, enc2, enc3 = \
        textChop(allKeys, allEnc, chacha_start_index, chacha_end_index, aes_end_index, des_end_index)

    msg1 = dec_ChaCha(key1, nonce1, enc1)
    msg2 = dec_AES(key2, nonce2, enc2)
    msg3 = dec_DES(key3, nonce3, enc3)

    print((msg1+msg2+msg3).decode("utf-8"))

ownerSendMKey()
print("Hello, this is a break")
master_key = userReceiveMKey()
grouped_keys = userDecKeys(master_key)
decrypt(grouped_keys)