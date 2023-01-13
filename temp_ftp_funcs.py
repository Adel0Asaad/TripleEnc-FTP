import ftplib

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
    filename = "FileToUpload.txt" 
    with open("Downloaded File", "wb") as file: 
        # use FTP's RETR command to download the file 
        ftp.retrbinary(f"RETR {filename}", file.write) 
    # quit and close the connection 
    ftp.quit()
