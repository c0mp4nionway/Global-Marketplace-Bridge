from cryptography.fernet import Fernet
import os

class EncryptionUtils:
    @staticmethod
    def generate_key():
        """Generate a new Fernet key and save it to a file."""
        key = Fernet.generate_key()
        with open('secret.key', 'wb') as key_file:
            key_file.write(key)

    @staticmethod
    def load_key():
        """Load the Fernet key from the current directory."""
        return open('secret.key', 'rb').read()

    @staticmethod
    def encrypt_data(data: str) -> bytes:
        """Encrypt the given data using the Fernet key."""
        key = EncryptionUtils.load_key()
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(data.encode())
        return encrypted_data

    @staticmethod
    def decrypt_data(encrypted_data: bytes) -> str:
        """Decrypt the given data using the Fernet key."""
        key = EncryptionUtils.load_key()
        fernet = Fernet(key)
        decrypted_data = fernet.decrypt(encrypted_data).decode()
        return decrypted_data