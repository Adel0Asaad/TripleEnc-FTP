from codecs import ascii_encode
import tkinter as tk
import threading
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tokenize import String
from xml.etree.ElementTree import tostring
import ftplib


#
#   Our GUI thread (text editor application)
#

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
    filename = "sometextfile.txt" 
    with open(filename, "rb") as file: 
        # use FTP's STOR command to upload the file 
        ftp.storbinary(f"STOR {filename}", file) 
    # quit and close the connection 
    ftp.quit()

def download():
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
    filename = "anothertextfile.txt" 
    with open(filename, "wb") as file: 
        # use FTP's RETR command to download the file 
        ftp.retrbinary(f"RETR {filename}", file.write) 
    # quit and close the connection 
    ftp.quit()

def textApp():


    window = tk.Tk()
    window.title("Team 28 Client")
    window.rowconfigure(0, minsize=800, weight=1)
    window.columnconfigure(1, minsize=800, weight=1)

    txt_edit = tk.Text(window, bg="#242424", fg="#FFFFFF", insertbackground="#CCCCCC")
    fr_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)
    btn_open = tk.Button(fr_buttons, text="Connect")
    btn_save = tk.Button(fr_buttons, text="Save As...")
    btn_add_text = tk.Button(fr_buttons, text="Insert Hello")

    btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    btn_save.grid(row=1, column=0, sticky="ew", padx=5)
    btn_add_text.grid(row=2, column=0, sticky="ew", padx=5, pady=10)

    fr_buttons.grid(row=0, column=0, sticky="ns")
    
    window.mainloop()


print('Now we can continue running code while mainloop runs!')

textThread = threading.Thread(target=textApp)
textThread.start()