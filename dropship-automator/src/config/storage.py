from cryptography.fernet import Fernet
import os
import json

class ConfigStorage:
    def __init__(self, config_file: str, key_file: str):
        self.config_file = config_file
        self.key_file = key_file
        self.fernet = self.load_or_create_key()

    def load_or_create_key(self):
        if not os.path.exists(self.key_file):
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
        with open(self.key_file, 'rb') as f:
            return Fernet(f.read())

    def load_config(self):
        if not os.path.exists(self.config_file):
            return {}
        with open(self.config_file, 'rb') as f:
            encrypted_data = f.read()
        decrypted_data = self.fernet.decrypt(encrypted_data)
        return json.loads(decrypted_data)

    def save_config(self, config: dict):
        encrypted_data = self.fernet.encrypt(json.dumps(config).encode('utf-8'))
        with open(self.config_file, 'wb') as f:
            f.write(encrypted_data)