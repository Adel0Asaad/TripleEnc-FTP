from Crypto.PublicKey import RSA

oKey = RSA.generate(2048)
oprivate_key = oKey.export_key()
file_out = open("owner_private.pem", "wb")
file_out.write(oprivate_key)
file_out.close()

opublic_key = oKey.publickey().export_key()
file_out = open("owner_receiver.pem", "wb")
file_out.write(opublic_key)
file_out.close()

uKey = RSA.generate(2048)
uprivate_key = uKey.export_key()
file_out = open("user_private.pem", "wb")
file_out.write(uprivate_key)
file_out.close()

upublic_key = uKey.publickey().export_key()
file_out = open("user_receiver.pem", "wb")
file_out.write(upublic_key)
file_out.close()