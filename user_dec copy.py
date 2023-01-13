from Crypto.PublicKey import RSA
from Crypto.Cipher import ChaCha20_Poly1305, AES, DES, PKCS1_OAEP, Salsa20

def decrypt():

        ################################################ MasterKey Handling ################################################

    def ownerSendMKey():

        key_in = open("masterKey.bin", "rb")
        finalKey =  key_in.read()
        key_in.close()
        recepient_key = RSA.import_key(open("user_receiver.pem").read())
        cipher_rsa_user_public = PKCS1_OAEP.new(recepient_key)
        encKey = cipher_rsa_user_public.encrypt(finalKey)

        key_out = open("pp_mKey.bin", "wb")
        key_out.write(encKey)
        key_out.close()

    def userReceiveMKey():

        key_in = open("loc_master_key.bin", "rb")
        finalKey =  key_in.read()
        key_in.close()

        private_key = RSA.import_key(open("user_private.pem").read())
        cipher_rsa_user_private = PKCS1_OAEP.new(private_key)
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

    ################################################ MasterKey Handling ################################################

    ################################################     DECRYPTIONS    ################################################

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

    ################################################     DECRYPTIONS    ################################################

    def textChop(keys, text):

        text1 = text2 = text3 = b''
        for myByte in [ text[x].to_bytes(1,"big") for x in range(len(text)) if x%3==0 ]:
            text1 += myByte
        for myByte in [ text[x].to_bytes(1,"big") for x in range(len(text)) if x%3==1 ]:
            text2 += myByte
        for myByte in [ text[x].to_bytes(1,"big") for x in range(len(text)) if x%3==2 ]:
            text3 += myByte

        key1, key2, key3 = \
            [ keys[x:y] for x,y in ((0, 32), (32, 48), (48, 56)) ]

        return key1, key2, key3, text1, text2, text3

    def textRePerm(text):
        myBArr = bytearray(text)
        for x in range(len(text)):
            myBArr[(x*3)%len(text)] = text[x]
        text = b''
        for myByte in myBArr:
            text += myByte.to_bytes(1, "big")
        return text

    def dec_logic(allKeys):
        
        data_in = open("encrypted_data.bin", "rb")
        nonce1, nonce2, nonce3, allEnc = \
            [ data_in.read(x) for x in (12, 16, 16, -1) ]
        data_in.close()

        key1, key2, key3, enc1, enc2, enc3 = textChop(allKeys, allEnc)
        
        msg1 = dec_ChaCha(key1, nonce1, enc1)
        msg2 =    dec_AES(key2, nonce2, enc2)
        msg3 =    dec_DES(key3, nonce3, enc3)

        finalMsg = textRePerm(msg1+msg2+msg3)
        print(finalMsg.decode("utf-8"))

    ownerSendMKey()
    master_key = userReceiveMKey()
    grouped_keys = userDecKeys(master_key)
    dec_logic(grouped_keys)
