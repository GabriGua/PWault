import argon2
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def derive_key(secret, salt):
    result = argon2.low_level.hash_secret_raw(
        secret.encode(), salt,
        time_cost=3, memory_cost=65000, parallelism=1, hash_len=32, type=argon2.low_level.Type.ID)
    return result

def encrypt(data, key):
    nonce = os.urandom(12)
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, data, None)
    blob = nonce + ciphertext
    return blob

def decrypt(blob, key):

    nonce = blob[:12]
    ciphertext = blob[12:]
    aesgcm = AESGCM(key)
    pw = aesgcm.decrypt(nonce, ciphertext, None)
    return pw

