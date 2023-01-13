import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import time

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
