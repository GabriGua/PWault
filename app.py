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
            self.key = key
            self.entries = load_vault(self.key, VAULT_PATH)
            self.onLine = True
            self.show_vault_screen()
            self.status_label = customtkinter.CTkLabel(self, text="[✓] Login successfully", font=("Roboto Medium", 30), fg_color= "#CBEF43", text_color="black", corner_radius=10)
            self.status_label.grid(row=2, column=0, columnspan=5, pady=(5,10), sticky="nsew")
            self.after(2000, lambda: self.status_label.destroy())
        except InvalidTag:
            self.status_label = customtkinter.CTkLabel(self, text="[✗] Wrong password", font=("Roboto Medium", 30), fg_color= "#CBEF43", text_color="black", corner_radius=10)
            self.status_label.grid(row=2, column=0, columnspan=5, pady=30, sticky="nsew")
            self.after(2000, lambda: self.status_label.destroy())
        

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()        

    def show_vault_screen(self):
        self.clear_screen()
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=2)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)

        # Sidebar Frame
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0, fg_color="#3F4045")
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Vault", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="new")
        self.button_add = customtkinter.CTkButton(self, text="Add Entry", command=self.button_add_callback)
        self.button_add.grid(row=1, column=0, padx=10, pady=(100, 0), sticky="new")
        self.button_gen = customtkinter.CTkButton(self, text="Generate Password")
        self.button_gen.grid(row=2, column=0, padx=10, pady=(0, 100), sticky="new")
        self.button_exit = customtkinter.CTkButton(self, text="Exit", command=self.button_exit_callback)
        self.button_exit.grid(row=3, column=0, padx=10, pady=(25, 10), sticky="sew")

        

        # create scrollable frame
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="Your Password List", fg_color="#30292F")
        self.scrollable_frame.grid(row=1, column=1, columnspan=4, rowspan=4, padx=0, pady=0, sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame_switches = []
        for self.entry in self.entries:
            i = self.entries.index(self.entry)
            self.Entry = customtkinter.CTkLabel(master=self.scrollable_frame, text=f"{self.entry.name}", width=120, height=25, corner_radius=8, fg_color=("white", "#72A98F"), font=("Roboto Medium", 16))
            self.Entry.grid(row=i, column=1, padx=10, pady=(0, 20))
            self.scrollable_frame_switches.append(self.Entry)
        

        # Search Bar
        self.sidebar_frame = customtkinter.CTkFrame(self, height=40, corner_radius=0, fg_color="#30292F")
        self.sidebar_frame.grid(row=0, column=1, columnspan=4, sticky="nsew")
        self.search_entry = customtkinter.CTkEntry(self, placeholder_text="Search Entry")
        self.search_entry.grid(row=0, column=1, columnspan=1, padx=10, pady=(20, 10), ipadx=100, ipady=5, sticky="ew")
        self.button_get = customtkinter.CTkButton(self, text="Find Entry")
        self.button_get.grid(row=0, column=3, padx=10, pady=(25, 10), sticky="ew")
        

        #self.button_delete = customtkinter.CTkButton(self, text="Delete Entry")
        #self.button_delete.grid(row=1, column=4, padx=10, pady=10, sticky="nsew")

    def button_add_callback(self):
        self.clear_screen()
        self.entry_name = customtkinter.CTkEntry(self, placeholder_text="Service Name")
        self.entry_name.grid(row=0, column=0, padx=10, pady=10)
        self.entry_username = customtkinter.CTkEntry(self, placeholder_text="Username (optional)")
        self.entry_username.grid(row=1, column=0, padx=10, pady=10)
        self.entry_password = customtkinter.CTkEntry(self, placeholder_text="Password", show="*")
        self.entry_password.grid(row=2, column=0, padx=10, pady=10)
        self.entry_notes = customtkinter.CTkEntry(self, placeholder_text="Notes (optional)")
        self.entry_notes.grid(row=3, column=0, padx=10, pady=10)
        self.button_save = customtkinter.CTkButton(self, text="Save Entry", command = self.button_save_callback)
        self.button_save.grid(row=4, column=0, padx=10, pady=10)

    def button_exit_callback(self):
        self.destroy()
        print("Exiting the application...")

    def button_save_callback(self):
        name = self.entry_name.get()
        username = self.entry_username.get()
        password = self.entry_password.get()
        notes = self.entry_notes.get() or None
        entry = Entry(name = name, username = username, password = password, notes = notes)
        self.entries.append(entry)
        save_vault(self.entries, self.key, VAULT_PATH)
        self.show_vault_screen()
        self.status_label = customtkinter.CTkLabel(self, text="[✓] saved successfully", font=("Roboto Medium", 30), fg_color= "#CBEF43", text_color="black", corner_radius=10)
        self.status_label.grid(row=2, column=0, columnspan=5, pady=(5,10), sticky="nsew")
        self.after(2000, lambda: self.status_label.destroy())

    
app = App()
app.mainloop()