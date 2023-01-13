import tkinter as tk
from PIL import ImageTk
import threading
import ftplib
import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, ChaCha20_Poly1305, AES, DES, Salsa20
from Crypto.Random import get_random_bytes
from os import system

#
#   Our GUI thread (text editor application)
#

def clear():
    system("cls")

def initConnThread(): # TODO: create a function like this for each command below (download/upload) in case it takes too much time, we don't want it to clog the GUI
    threading.Thread(target=initConn).start()

def initConn():
    PORT = 5050
    SERVER = "127.0.0.1"
    ADDR = (SERVER, PORT)
    
    def getMasterKey():
        key_in = open("masterKey.bin", "rb")
        master_key = key_in.read()
        key_in.close()
        print(master_key)
        return master_key

    def enc_RSA(pubKey, masterKey):
        public_key = RSA.import_key(pubKey)
        cipher = PKCS1_OAEP.new(public_key)
        result = cipher.encrypt(masterKey)
        return result

    master_key = getMasterKey()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind(ADDR)
        server.listen()
    except Exception as e:
        print(e)
    else:
        clientSocket, clientAddr = server.accept()
        public_key = clientSocket.recv(450) # the public key file is always 450 bytes.
        encKey = enc_RSA(public_key, master_key)
        clientSocket.send(encKey)

def encryptThread():
    threading.Thread(target=encrypt).start()

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

def uploadThread():
    threading.Thread(target=upload).start()

def upload():
    # FTP server credentials
    FTP_HOST = "127.0.0.1"
    FTP_PORT = 6060
    FTP_USER = "username"
    FTP_PASS = "P@ssw0rd"
    # connect to the FTP server 
    ftp = ftplib.FTP() 
    ftp.connect(FTP_HOST,FTP_PORT) 
    ftp.login(FTP_USER,FTP_PASS) 
    # force UTF-8 encoding 
    ftp.encoding = "utf-8" 
    # local file name you want to upload 
    filename = "FileToUpload.txt" 
    ftp.cwd("/htdocs")
    with open(filename, "rb") as file: 
        # use FTP's STOR command to upload the file 
        ftp.storbinary(f"STOR {filename}", file) 
    # quit and close the connection 
    print('Should be uploaded')

    ftp.quit()

def on_enter(e):
    e.widget['background'] = "#075ea1"

def on_leave(e):
    e.widget['background'] = 'SystemButtonFace'

def textApp():
    
    window = tk.Tk()
    window.title("Security Project")
    window.rowconfigure(0, minsize=600, weight=1)
    window.columnconfigure(1, minsize=200, weight=1)
    # window.protocol("WM_DELETE_WINDOW", on_closing)
    window.geometry("800x600")
    window.minsize(800, 600)
    window.resizable(False, False)

    # txt_edit = tk.CustomText(window, bg="#242424", fg="#FFFFFF", insertbackground="#DDDDDD", wrap= tk.WORD, font=("Consolas", 13), state=tk.DISABLED)
    team_frame = tk.Frame(window, relief=tk.RAISED, bd=10, bg="#242424")

    fr_buttons = tk.Frame(window, relief=tk.RAISED, bd=10, bg="#242424")
    # lab_team = tk.Label (fr_buttons, text="Team 28", fg="#075ea1", bg="#000000", font=("Times New Roman", 25, tk.UNDERLINE))
    pixelVirtual = tk.PhotoImage(width=1, height=1)
    lab_upload = tk.Label (fr_buttons, bg="#242424",fg="#FFFFFF", text="Press to upload the file", font=("Times New Roman", 14))
    btn_upload = tk.Button(fr_buttons, text="Upload", command=uploadThread, width=90, compound="c", image=pixelVirtual, bg="#a6a6a6")
    lab_master = tk.Label (fr_buttons, bg="#242424",fg="#FFFFFF", text="Press to listen for a user (to send a master key)", font=("Times New Roman", 14))
    btn_master = tk.Button(fr_buttons, text="Listen", command=initConnThread, width=90, compound="c", image=pixelVirtual, bg="#a6a6a6")
    lab_encrypt = tk.Label (fr_buttons, bg="#242424",fg="#FFFFFF", text="Press to encrypt the file", font=("Times New Roman", 14))
    btn_encrypt = tk.Button(fr_buttons, text="Encrypt", command=encryptThread, width=90, compound="c", image=pixelVirtual, bg="#a6a6a6")

    btn_upload.bind("<Enter>", on_enter)
    btn_upload.bind("<Leave>", on_leave)
    btn_master.bind("<Enter>", on_enter)
    btn_master.bind("<Leave>", on_leave)
    btn_encrypt.bind("<Enter>", on_enter)
    btn_encrypt.bind("<Leave>", on_leave)

    photo = ImageTk.PhotoImage(file= "ASUENG Logo.png")
    imageLabel = tk.Label(team_frame, bg="#242424", image = photo)
    imageLabel.image = photo

    lab_encrypt.grid(row=1,column=0, padx=5, pady=(50,20))
    btn_encrypt.grid(row=2, column=0, padx=5, pady=0)
    lab_upload.grid(row=3,column=0, padx=5, pady=(50,20))
    btn_upload.grid(row=4, column=0, padx=5, pady=0)
    lab_master.grid(row=5,column=0, padx=5, pady=(50,20))
    btn_master.grid(row=6, column=0, padx=5, pady=0)
    imageLabel.grid(row=0, column=0, padx=95, pady=320)

    fr_buttons.grid(row=0, column=0, sticky="ns")
    team_frame.grid(row=0, column=1, sticky="nsew")

    window.mainloop()

textThread = threading.Thread(target=textApp)
textThread.start()