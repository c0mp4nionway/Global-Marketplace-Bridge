import unittest
from src.utils.encryption import encrypt_config, decrypt_config, load_or_create_key

class TestEncryption(unittest.TestCase):

    def setUp(self):
        self.key = load_or_create_key()
        self.sample_data = {
            'api_keys': {
                'ebay': 'test_ebay_key',
                'aliexpress': 'test_aliexpress_key'
            },
            'settings': {
                'use_sandbox': True,
                'markup_percent': 30.0
            }
        }

    def test_encrypt_decrypt(self):
        encrypted = encrypt_config(self.sample_data)
        decrypted = decrypt_config(encrypted)
        self.assertEqual(decrypted, self.sample_data)

    def test_load_or_create_key(self):
        key = load_or_create_key()
        self.assertIsNotNone(key)

if __name__ == '__main__':
    unittest.main()