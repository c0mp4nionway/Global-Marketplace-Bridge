import unittest
from src.gui.app import AppGUI
from src.config.storage import load_config

class TestAppGUI(unittest.TestCase):
    def setUp(self):
        self.cfg = load_config()
        self.app = AppGUI(self.cfg)

    def test_initialization(self):
        self.assertIsNotNone(self.app)
        self.assertEqual(self.app.title(), 'Dropship Automator - Clean Full')

    def test_config_wizard(self):
        # Simulate running the configuration wizard
        self.app.worker.start_auto_sync()
        self.assertTrue(self.app.worker._stop_event.is_set() is False)

    def test_import_single(self):
        # Test importing a single product
        ali_id = '1234567890'
        self.app.ali_entry.insert(0, ali_id)
        self.app.import_single()
        # Check if the log contains the import message
        self.assertIn(f'Imported {ali_id}', self.app.logbox.get('1.0', 'end'))

    def test_import_csv(self):
        # Test importing from a CSV file
        # Assuming a valid CSV file path is provided
        self.app.import_csv()
        # Check if the log contains the CSV import results message
        self.assertIn('CSV import results:', self.app.logbox.get('1.0', 'end'))

    def test_sync_now(self):
        # Test the sync now functionality
        self.app.sync_now()
        # Check if the log contains the sync completed message
        self.assertIn('Stock sync completed', self.app.logbox.get('1.0', 'end'))

if __name__ == '__main__':
    unittest.main()