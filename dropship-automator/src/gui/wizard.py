from tkinter import Tk, Label, Entry, Button, messagebox
import json
import os
from cryptography.fernet import Fernet
from src.config.storage import load_config, save_config

class ConfigWizard:
    def __init__(self, master):
        self.master = master
        self.master.title("Configuration Wizard")
        self.config = load_config()

        Label(master, text="eBay Client ID:").grid(row=0)
        self.ebay_client_id_entry = Entry(master)
        self.ebay_client_id_entry.grid(row=0, column=1)

        Label(master, text="eBay Client Secret:").grid(row=1)
        self.ebay_client_secret_entry = Entry(master)
        self.ebay_client_secret_entry.grid(row=1, column=1)

        Label(master, text="AliExpress App Key:").grid(row=2)
        self.ali_app_key_entry = Entry(master)
        self.ali_app_key_entry.grid(row=2, column=1)

        Label(master, text="AliExpress App Secret:").grid(row=3)
        self.ali_app_secret_entry = Entry(master)
        self.ali_app_secret_entry.grid(row=3, column=1)

        Button(master, text="Save Configuration", command=self.save_config).grid(row=4, columnspan=2)

    def save_config(self):
        self.config['ebay_client_id'] = self.ebay_client_id_entry.get()
        self.config['ebay_client_secret'] = self.ebay_client_secret_entry.get()
        self.config['ali_app_key'] = self.ali_app_key_entry.get()
        self.config['ali_app_secret'] = self.ali_app_secret_entry.get()

        save_config(self.config)
        messagebox.showinfo("Success", "Configuration saved successfully!")
        self.master.quit()

def run_wizard():
    root = Tk()
    wizard = ConfigWizard(root)
    root.mainloop()

if __name__ == "__main__":
    run_wizard()