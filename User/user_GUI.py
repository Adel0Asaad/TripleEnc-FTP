import tkinter as tk
from PIL import ImageTk
import threading
import ftplib
import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import ChaCha20_Poly1305, AES, DES, PKCS1_OAEP, Salsa20
import time
from os import system

#
#   Our GUI thread (text editor application)
#

def clear():
    system("cls")

def initConnThread(): # TODO: create a function like this for each command below (download/upload) in case it takes too much time, we don't want it to clog the GUI
    threading.Thread(target=initConn).start()

def initConn():
    done = False
    PORT = 5050
    SERVER = "127.0.0.1"
    ADDR = (SERVER, PORT)

    def getPubKey():
        key_in = open("user_receiver.pem")
        pubKey = key_in.read()
        key_in.close()
        return pubKey

    def dec_RSA(encKey):
        key_in = open("user_private.pem")
        prvKeyR = key_in.read()
        key_in.close()
        private_key = RSA.import_key(prvKeyR)
        cipher = PKCS1_OAEP.new(private_key)
        result = cipher.decrypt(encKey)
        return result

    public_key = getPubKey()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ctr = 0
    while((not done) & (ctr < 10)):
            
        try:
            print("Trying to connect")
            client.connect(ADDR)
            client.send(public_key.encode())
            msg = client.recv(1024)
        except Exception as e:
            print(e)
            print("Retrying in 5...")
            time.sleep(5)
            ctr += 1
        else:
            print("Connected with host!")
            master_key = dec_RSA(msg)
            print(master_key) # return this somewhere in the GUI app
            key_out = open("loc_master_key.bin", "wb")
            key_out.write(master_key)
            key_out.close()
            done = True
    if(not done):
        print("Connection timed out.")
    else:
        print("Retreived master key successfully!")
        print("Stored in: loc_master_key.bin")

def decryptThread():
    threading.Thread(target=decrypt).start()

def decrypt():

        ################################################ MasterKey Handling ################################################

    def userDecKeys():

        key_in = open("loc_master_key.bin", "rb")
        masterKey =  key_in.read()
        key_in.close()

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

    grouped_keys = userDecKeys()
    dec_logic(grouped_keys)

def downloadThread():
    threading.Thread(target=download).start()

def download():
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
    # the name of file you want to download from the FTP server 
    
    file1 = "encrypted_data.bin" 
    file2 = "encrypted_key.bin"
    with open(file1, "wb") as file: 
        # use FTP's STOR command to upload the file 
        ftp.retrbinary(f"RETR {file1}", file.write) 
    with open(file2, "wb") as file:
        ftp.retrbinary(f"RETR {file2}", file.write)
    # quit and close the connection 
    ftp.quit()

# def print_uploaded():
#     messagebox.showinfo("Message", "hi")

def on_enter(e):
    e.widget['background'] = "#075ea1"

def on_leave(e):
    e.widget['background'] = 'SystemButtonFace'

def textApp():
    
    window = tk.Tk()
    window.title("User Client")
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
    lab_download = tk.Label (fr_buttons, bg="#242424",fg="#FFFFFF", text="Press to download the file", font=("Times New Roman", 14))
    btn_download = tk.Button(fr_buttons, text="Download", command=downloadThread, width=90, compound="c", image=pixelVirtual, bg="#a6a6a6")
    lab_master = tk.Label (fr_buttons, bg="#242424", fg="#FFFFFF", text="Press to request the Master key", font=("Times New Roman", 14))
    btn_master = tk.Button(fr_buttons, text="Request Key", command=initConnThread, width=90, compound="c", image=pixelVirtual, bg="#a6a6a6")
    lab_decrypt = tk.Label (fr_buttons, bg="#242424", fg="#FFFFFF", text="Press to decrypt the file", font=("Times New Roman", 14))
    btn_decrypt = tk.Button(fr_buttons, text="Decrypt", command=decryptThread, width=90, compound="c", image=pixelVirtual, bg="#a6a6a6")

    lab_clear = tk.Label (fr_buttons, bg="#242424", fg="#FFFFFF", text="Press to clear the terminal screen", font=("Times New Roman", 14))
    btn_clear = tk.Button(fr_buttons, text="Clear", command=clear, width=90, compound="c", image=pixelVirtual, bg="#a6a6a6")

    btn_download.bind("<Enter>", on_enter)
    btn_download.bind("<Leave>", on_leave)
    btn_master.bind("<Enter>", on_enter)
    btn_master.bind("<Leave>", on_leave)
    btn_decrypt.bind("<Enter>", on_enter)
    btn_decrypt.bind("<Leave>", on_leave)
    btn_clear.bind("<Enter>", on_enter)
    btn_clear.bind("<Leave>", on_leave)

    photo = ImageTk.PhotoImage(file= "ASUENG Logo.png")
    imageLabel = tk.Label(team_frame, bg="#242424", image = photo)
    imageLabel.image = photo

    lab_download.grid(row=1,column=0, padx=5, pady=(50,20))
    btn_download.grid(row=2, column=0, padx=5, pady=0)
    lab_master.grid(row=3,column=0, padx=5, pady=(50,20))
    btn_master.grid(row=4, column=0, padx=5, pady=0)
    lab_decrypt.grid(row=5,column=0, padx=5, pady=(50,20))
    btn_decrypt.grid(row=6, column=0, padx=5, pady=0)
    lab_clear.grid(row=7,column=0, padx=5, pady=(50,20))
    btn_clear.grid(row=8, column=0, padx=5, pady=0)

    imageLabel.grid(row=0, column=0, padx=95, pady=320)

    fr_buttons.grid(row=0, column=0, sticky="ns")
    team_frame.grid(row=0, column=1, sticky="nsew")

    window.mainloop()

textThread = threading.Thread(target=textApp)
textThread.start()