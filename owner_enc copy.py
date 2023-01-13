from Crypto.Random import get_random_bytes
from Crypto.Cipher import ChaCha20_Poly1305, AES, DES, Salsa20



def encrypt():

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

    def textChop(text):

        text1 = text2 = text3 = b''
        for myByte in [ text[x].to_bytes(1,"big") for x in range(len(text)) if x%3==0 ]:
            text1 += myByte
        for myByte in [ text[x].to_bytes(1,"big") for x in range(len(text)) if x%3==1 ]:
            text2 += myByte
        for myByte in [ text[x].to_bytes(1,"big") for x in range(len(text)) if x%3==2 ]:
            text3 += myByte

        return text1, text2, text3

    def textRePerm(text):
        myBArr = bytearray(text)
        for x in range(len(text)):
            myBArr[(x*3)%len(text)] = text[x]
        text = b''
        for myByte in myBArr:
            text += myByte.to_bytes(1, "big")
        return text

    def enc_logic(plaintext):
        
        msg1, msg2, msg3 = textChop(plaintext)
        
        key1, nonce1, enc1 = enc_ChaCha(msg1)
        key2, nonce2, enc2 = enc_AES(msg2)
        key3, nonce3, enc3 = enc_DES(msg3)
        
        finalKey = key1 + key2 + key3
        finalNonce = nonce1 + nonce2 + nonce3
        prepermEnc = enc1 + enc2 + enc3
        finalEnc = textRePerm(prepermEnc)
        finalMsg = finalNonce + finalEnc

        masterKey, masterNonce, encKey = enc_Salsa(finalKey)

        keyMsg = masterNonce + encKey

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
    enc_logic(myText)