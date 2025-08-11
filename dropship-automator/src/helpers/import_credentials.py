import os
import json
from cryptography.fernet import Fernet
from src.config.storage import load_config, save_config

def import_credentials(api_key, api_secret, ebay_token):
    config = load_config()

    # Update the config with new credentials
    config['api']['aliexpress']['key'] = api_key
    config['api']['aliexpress']['secret'] = api_secret
    config['api']['ebay']['token'] = ebay_token

    # Save the updated config securely
    save_config(config)

if __name__ == "__main__":
    # Example usage: replace with actual input method
    api_key = input("Enter your AliExpress API Key: ")
    api_secret = input("Enter your AliExpress API Secret: ")
    ebay_token = input("Enter your eBay Token: ")

    import_credentials(api_key, api_secret, ebay_token)
    print("Credentials imported successfully.")