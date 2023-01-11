import ftplib
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
filename = "sometextfile.txt"
with open(filename, "rb") as file:
    # use FTP's STOR command to upload the file
    ftp.storbinary(f"STOR {filename}", file)
# quit and close the connection
ftp.quit()