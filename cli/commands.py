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
           
def add():
    pw = getpass.getpass()
    with open(VAULT_PATH, "rb") as f:
        content = f.read()
    salt = content[:16]
    key = derive_key(pw, salt)
    entries = load_vault(key, VAULT_PATH)
    
    name = input("name of the service: ")
    username = input("username (optional): ") or None
    password = getpass.getpass("password: ")
    notes = input("notes (optional): ") or None
    entry = Entry(name = name, username = username, password = password, notes = notes)
    entries.append(entry)
    save_vault(entries, key, VAULT_PATH)
    print("saved successfully")


def list_entries():
    pw = getpass.getpass()
    with open(VAULT_PATH, "rb") as f:
        content = f.read()
    salt = content[:16]
    key = derive_key(pw, salt)
    entries = load_vault(key, VAULT_PATH)

    for entry in entries:
        print(entry.name)

def get(name):
    pw = getpass.getpass()
    with open(VAULT_PATH, "rb") as f:
        content = f.read()
    salt = content[:16]
    key = derive_key(pw, salt)
    entries = load_vault(key, VAULT_PATH)

    for entry in entries:
        if entry.name == name:
            print(f"name: {entry.name}")
            print(f"username: {entry.username or 'N/A'}")
            print(f"password: {entry.password}")
            print(f"notes: {entry.notes or 'N/A'}")
            break

    else:
        print("not found")


def delete(name):
    pw = getpass.getpass()
    with open(VAULT_PATH, "rb") as f:
        content = f.read()
    salt = content[:16]
    key = derive_key(pw, salt)
    entries = load_vault(key, VAULT_PATH)

    for entry in entries:
        if entry.name == name:
            entries.remove(entry)
            save_vault(entries, key, VAULT_PATH)
            print("deleted successfully")
            break
    else:
        print("not found")
    