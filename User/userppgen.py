from Crypto.PublicKey import RSA

uKey = RSA.generate(2048)
uprivate_key = uKey.export_key()
file_out = open("user_private.pem", "wb")
file_out.write(uprivate_key)
file_out.close()

upublic_key = uKey.publickey().export_key()
file_out = open("user_receiver.pem", "wb")
file_out.write(upublic_key)
file_out.close()