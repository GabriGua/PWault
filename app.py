import customtkinter
from cli.commands import init, add, list_entries, get, delete, VAULT_PATH
from core.crypto import derive_key, encrypt, decrypt
from core.vault import create_vault, save_vault, load_vault
from core.models import Entry
from utils.generator import PassGenerator
from cryptography.exceptions import InvalidTag
import os
import getpass
import pyperclip

customtkinter.set_default_color_theme("green")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("900x600")
        self.title("PWault")
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=2)
        self.grid_columnconfigure(0, weight=1)

        



        self.label = customtkinter.CTkLabel(master=self, text="Welcome to PWault!", width=10, corner_radius=0, font=("Roboto Medium", 20) )
        self.label.grid(row=0, column=0,padx=20, pady=(10, 10), sticky="n")
        self.insertPW = customtkinter.CTkEntry(master=self, placeholder_text="Enter your password here", width=400, corner_radius=20, show="*" )
        self.insertPW.grid(row=1, column=0, padx=30, pady=30, sticky="n")




        self.button = customtkinter.CTkButton(self, text="Access Vault", command=self.button_callback)
        self.button.grid(row=2, column=0, padx=50, pady=(2, 2) , ipadx=200, sticky="n", ipady=20 )



    def button_callback(self):
        print("Accessing to the vault...")
        password = self.insertPW.get()
        
        with open(VAULT_PATH, "rb") as f:
            content = f.read()
            salt = content[:16]
        
        try:

            key = derive_key(password, salt)
            entries = load_vault(key, VAULT_PATH)
            onLine = True
            self.show_vault_screen()
        except InvalidTag:
            print("[✗] Wrong password")

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()        

    def show_vault_screen(self):
        self.clear_screen()
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)

        self.label = customtkinter.CTkLabel(self, text="Vault",  font=("Roboto Medium", 20))
        self.label.grid(pady=10, padx=10, row=0, column=0, columnspan=5, sticky="nsew")

        self.button_add = customtkinter.CTkButton(self, text="Add Entry")
        self.button_add.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.button_list = customtkinter.CTkButton(self, text="List Entries")
        self.button_list.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        self.button_gen = customtkinter.CTkButton(self, text="Generate Password")
        self.button_gen.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

        self.button_get = customtkinter.CTkButton(self, text="Find Entry")
        self.button_get.grid(row=1, column=3, padx=10, pady=10, sticky="nsew")

        self.button_delete = customtkinter.CTkButton(self, text="Delete Entry")
        self.button_delete.grid(row=1, column=4, padx=10, pady=10, sticky="nsew")

    
app = App()
app.mainloop()