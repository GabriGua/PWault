import os
import getpass
from core.crypto import derive_key, encrypt, decrypt
from core.vault import create_vault, save_vault, load_vault
from core.models import Entry

VAULT_PATH = os.path.join(os.environ["APPDATA"], "PWault", "vault.bin")

def init():
    if(os.path.exists(VAULT_PATH)):
        print("vault already exists")
    else:
        os.makedirs(os.path.dirname(VAULT_PATH), exist_ok=True)
        pw = getpass.getpass()
        try_pw = getpass.getpass()
        if(pw == try_pw):
           salt = os.urandom(16)

           key = derive_key(pw, salt)
           create_vault(key, VAULT_PATH)
           print("Init successful!")
        else:
            print("passwords do not match, try again")
           