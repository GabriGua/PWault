import os
import getpass
from core.crypto import derive_key, encrypt, decrypt
from core.vault import create_vault, save_vault, load_vault
from core.models import Entry
import pyperclip


VAULT_PATH = os.path.join(os.environ["APPDATA"], "PWault", "vault.bin")

def init():
    
    
        os.makedirs(os.path.dirname(VAULT_PATH), exist_ok=True)
        pw = getpass.getpass()
        try_pw = getpass.getpass()
        if(pw == try_pw):
           salt = os.urandom(16)

           key = derive_key(pw, salt)
           create_vault(key, VAULT_PATH, salt)
           print("[✓] Init successful!")
        else:
            print("[✗] passwords do not match, try again")
           
def add(entries, key):
    
    
    
    while True:
        name = input("name of the service: ")
        if name != None:

            break

    username = input("username (optional): ") or None
    while True:
        password = getpass.getpass("password: ")
        if password != "":

            break
    

    
    notes = input("notes (optional): ") or None
    entry = Entry(name = name, username = username, password = password, notes = notes)
    entries.append(entry)
    save_vault(entries, key, VAULT_PATH)
    print("[✓] saved successfully")
    os.system('pause')
    os.system('cls')
    


def list_entries(entries):
    for entry in entries:
        print(entry.name)
        os.system('pause')
        os.system('cls')
    

def get(name, entries):

    for entry in entries:
        if entry.name == name:
            print("─" * 40)
            print(f"username: {entry.username or 'N/A'}")
            print(f"password: {entry.password}")
            pyperclip.copy(entry.password)
            print(f"notes: {entry.notes or 'N/A'}")
            print("[✓] pw copied into clipboard!")
            os.system('pause')
            os.system('cls')
            break

    else:
        print("[✗] not found")
        os.system('pause')
        os.system('cls')
    


def delete(name, entries, key):
    
    next = input("Are you sure you want to delete " + name + "? (yes/no): ")
    if next.lower() == "yes":
        for entry in entries:
            if entry.name == name:
                entries.remove(entry)
                save_vault(entries, key, VAULT_PATH)
                print("[✓] deleted successfully")
                os.system('pause')
                os.system('cls')
                break
        else:
            print("[✗] not found")
            os.system('pause')
            os.system('cls')


    else:
        print("[✗] operation cancelled")
        os.system('pause')
        os.system('cls')
    