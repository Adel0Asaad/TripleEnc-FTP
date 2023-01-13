from codecs import ascii_encode
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
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
    FTP_HOST = "ftp.byethost14.com" 
    FTP_PORT = 21 
    FTP_USER = "b14_33366562" 
    FTP_PASS = "7odazftt" 
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

def download():
    FTP_HOST = "ftp.byethost14.com" 
    FTP_PORT = 21 
    FTP_USER = "b14_33366562" 
    FTP_PASS = "7odazftt" 
    # connect to the FTP server 
    ftp = ftplib.FTP() 
    ftp.connect(FTP_HOST,FTP_PORT) 
    ftp.login(FTP_USER,FTP_PASS) 
    # force UTF-8 encoding 
    ftp.encoding = "utf-8" 
    # the name of file you want to download from the FTP server 
    filename = "FileToUpload.txt" 
    with open("Downloaded File", "wb") as file: 
        # use FTP's RETR command to download the file 
        ftp.retrbinary(f"RETR {filename}", file.write) 
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
    window.title("Security Project")
    window.rowconfigure(0, minsize=600, weight=1)
    window.columnconfigure(1, minsize=200, weight=1)
    # window.protocol("WM_DELETE_WINDOW", on_closing)
    window.geometry("800x600")
    window.minsize(800, 600)
    window.resizable(False, False)

    # txt_edit = tk.CustomText(window, bg="#242424", fg="#FFFFFF", insertbackground="#DDDDDD", wrap= tk.WORD, font=("Consolas", 13), state=tk.DISABLED)
    team_frame = tk.Frame(window, relief=tk.RAISED, bd=10, bg="#242424")
    team_members_label= tk.Label(team_frame, bg="#242424", fg="#075ea1", text="Team Members", font=("Times New Roman", 32))
    adel_asaad_label= tk.Label(team_frame, bg="#242424", fg="#FFFFFF", text="Adel Asaad - 18P2949", font=("Times New Roman", 18))
    madonna_bassem_label= tk.Label(team_frame, bg="#242424", fg="#FFFFFF", text="Madonna Bassem - 185194", font=("Times New Roman", 18))
    mohamed_adel_label= tk.Label(team_frame, bg="#242424", fg="#FFFFFF", text="Mohamed Adel - 18P1724", font=("Times New Roman", 18))

    fr_buttons = tk.Frame(window, relief=tk.RAISED, bd=10, bg="#242424")
    # lab_team = tk.Label (fr_buttons, text="Team 28", fg="#075ea1", bg="#000000", font=("Times New Roman", 25, tk.UNDERLINE))
    lab_upload = tk.Label (fr_buttons, bg="#242424",fg="#FFFFFF", text="Press to encrypt & upload the file", font=("Times New Roman", 14))
    lab_download = tk.Label (fr_buttons, bg="#242424",fg="#FFFFFF", text="Press to decrypt & download the file", font=("Times New Roman", 14))
    pixelVirtual = tk.PhotoImage(width=1, height=1)
    btn_download = tk.Button(fr_buttons, text="Download", command=download, width=90, compound="c", image=pixelVirtual, bg="#a6a6a6")
    btn_upload = tk.Button(fr_buttons, text="Upload", command=upload, width=90, compound="c", image=pixelVirtual, bg="#a6a6a6")

    btn_download.bind("<Enter>", on_enter)
    btn_download.bind("<Leave>", on_leave)
    btn_upload.bind("<Enter>", on_enter)
    btn_upload.bind("<Leave>", on_leave)

    photo = ImageTk.PhotoImage(file= "ASUENG Logo.png")
    imageLabel = tk.Label(fr_buttons, bg="#242424", image = photo)
    imageLabel.image = photo

    lab_upload.grid(row=1,column=0, padx=5, pady=(50,20))
    btn_upload.grid(row=2, column=0, padx=5, pady=0)
    lab_download.grid(row=3,column=0, padx=5, pady=(50,20))
    btn_download.grid(row=4, column=0, padx=5, pady=10)
    imageLabel.grid(row=6, column=0, pady=60)

    team_members_label.place(relx=0.5, rely=0.1, anchor="center")
    adel_asaad_label.place(relx=0.5, rely=0.3, anchor="center")
    madonna_bassem_label.place(relx=0.5, rely=0.45, anchor="center")
    mohamed_adel_label.place(relx=0.5, rely=0.6, anchor="center")

    fr_buttons.grid(row=0, column=0, sticky="ns")
    team_frame.grid(row=0, column=1, sticky="nsew")

    window.mainloop()


print('Now we can continue running code while mainloop runs!')

textThread = threading.Thread(target=textApp)
textThread.start()