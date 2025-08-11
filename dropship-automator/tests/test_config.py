import unittest
from src.config.storage import load_config, save_config
from src.config.schema import ConfigSchema

class TestConfig(unittest.TestCase):

    def setUp(self):
        self.config = {
            'api': {
                'ebay': {
                    'client_id': 'test_client_id',
                    'client_secret': 'test_client_secret',
                    'sandbox': True
                },
                'aliexpress': {
                    'app_key': 'test_app_key',
                    'app_secret': 'test_app_secret'
                }
            }
        }

    def test_load_config(self):
        # Test loading the default configuration
        config = load_config()
        self.assertIsInstance(config, dict)
        self.assertIn('api', config)

    def test_save_config(self):
        # Test saving the configuration
        save_config(self.config)
        loaded_config = load_config()
        self.assertEqual(loaded_config, self.config)

    def test_config_schema(self):
        # Test the configuration schema
        schema = ConfigSchema()
        self.assertTrue(schema.validate(self.config))

if __name__ == '__main__':
    unittest.main()