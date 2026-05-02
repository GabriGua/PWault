from cli.commands import init, add, list_entries, get, delete, VAULT_PATH
from core.crypto import derive_key, encrypt, decrypt
from core.vault import create_vault, save_vault, load_vault
from core.models import Entry
from utils.generator import PassGenerator
from cryptography.exceptions import InvalidTag
import os
import getpass
import pyperclip



if(os.path.exists(VAULT_PATH)):
    print("vault already exists")
    pw = getpass.getpass()
    with open(VAULT_PATH, "rb") as f:
        content = f.read()
    salt = content[:16]
    
    try:

        key = derive_key(pw, salt)
        entries = load_vault(key, VAULT_PATH)
        onLine = True
        os.system('cls')
        print("Welcome to your vault") 
        while(onLine == True):
            
            print("Digit one of the following commands: Add, Gen, List, Get, Delete, Exit")
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
                delete(name, entries, key)

            elif(command == "Gen" or command == "gen"):
                
                try: 
                    length = int(input("Insert the password length: "))
                    result = PassGenerator(length)
                    print(result)
                    pyperclip.copy(result)
                    print("[✓] copied into clipboard!")
                    os.system('pause')
                    os.system('cls')
                    

                except:
                    print("[✗] you didn't enter a number")
                
            
            elif(command == "Exit" or command == "exit"):
                onLine = False
            
            else:
                os.system('cls')

            


        print("[✓] Logout Successfull")
    except InvalidTag:
        print("[✗] Wrong password")
        exit()

    

else:
    init()

