from core.crypto import derive_key, encrypt, decrypt
import os

salt = os.urandom(12)

secret = input("metti master password ")
key = derive_key(secret, salt)

data = input("stringa di prova ")

blob = encrypt(data.encode(), key)
print(blob)

pw = decrypt(blob, key)
print(pw.decode())