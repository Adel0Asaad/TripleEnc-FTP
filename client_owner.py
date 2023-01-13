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


def initConn():
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

initConn()