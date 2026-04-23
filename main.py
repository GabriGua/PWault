from cli.commands import init, add, list_entries, get, delete, VAULT_PATH
from core.crypto import derive_key, encrypt, decrypt
from core.vault import create_vault, save_vault, load_vault
from core.models import Entry
import os
import getpass



if(os.path.exists(VAULT_PATH)):
    print("vault already exists")
    pw = getpass.getpass()
    with open(VAULT_PATH, "rb") as f:
        content = f.read()
    salt = content[:16]
    key = derive_key(pw, salt)
    entries = load_vault(key, VAULT_PATH)
    onLine = True
    print("Welcome to your vault") 
    while(onLine == True):
        
        print("Digit one of the following commands: Add, List, Get, Delete, Exit")
        command = input("Insert command: ")
        if(command == "Add" or command == "add") :
            add(entries, key)
            
        elif(command == "List" or command == "list"):
            list_entries(entries)
        
        elif(command == "Get" or command == "get"):
            name = input("Enter the name: ")
            get(name, entries)
        
        elif(command == "Delete" or command == "delete"):
            name = input("Enter the name: ")
            delete(name, entries)
        elif(command == "Exit" or command == "exit"):
            onLine = False

    print("Logout Successfull")
    

else:
    init()

