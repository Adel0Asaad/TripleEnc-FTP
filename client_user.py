import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MSG = '!disconnect'
SERVER = "127.0.0.1"
ADDR = (SERVER, PORT)
REQUEST_C_MSG = '!requestconnect'

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

def initConn():
    public_key = getPubKey()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(ADDR)
        client.send(public_key.encode())
        msg = client.recv(1024)
    except Exception as e:
        print(e)
    else:
        master_key = dec_RSA(msg)
        print(master_key)

initConn()