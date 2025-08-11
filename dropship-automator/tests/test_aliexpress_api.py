import unittest
from src.api.aliexpress import AliExpressAPI

class TestAliExpressAPI(unittest.TestCase):

    def setUp(self):
        # Initialize the AliExpressAPI with mock configuration
        self.config = {
            'ali_app_key': 'test_key',
            'ali_app_secret': 'test_secret',
            'use_sandbox': True
        }
        self.api = AliExpressAPI(self.config)

    def test_fetch_product(self):
        # Test fetching a product with a known ID
        ali_id = '123456'
        product = self.api.fetch_product(ali_id)
        self.assertIn('aliexpress_affiliate_productdetail_get_response', product)
        self.assertIn('resp_result', product['aliexpress_affiliate_productdetail_get_response'])
        self.assertIn('result', product['aliexpress_affiliate_productdetail_get_response']['resp_result'])
        self.assertIn('products', product['aliexpress_affiliate_productdetail_get_response']['resp_result']['result'])
        self.assertGreater(len(product['aliexpress_affiliate_productdetail_get_response']['resp_result']['result']['products']), 0)

    def test_invalid_product_id(self):
        # Test fetching a product with an invalid ID
        ali_id = 'invalid_id'
        with self.assertRaises(ValueError):
            self.api.fetch_product(ali_id)

if __name__ == '__main__':
    unittest.main()