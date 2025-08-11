import unittest
from src.api.ebay import EbayAPI

class TestEbayAPI(unittest.TestCase):
    def setUp(self):
        self.config = {
            'ebay_client_id': 'test_client_id',
            'ebay_client_secret': 'test_client_secret',
            'ebay_token': 'test_token',
            'use_sandbox': True
        }
        self.ebay_api = EbayAPI(self.config)

    def test_create_inventory_item(self):
        sku = 'TEST-SKU'
        payload = {
            'sku': sku,
            'product': {
                'title': 'Test Product',
                'description': 'Test Description',
                'imageUrls': ['http://example.com/image.jpg'],
                'aspects': {}
            },
            'availability': {'shipToLocationAvailability': {'quantity': 10}}
        }
        response = self.ebay_api.create_inventory_item(sku, payload)
        self.assertEqual(response['sku'], sku)

    def test_create_offer(self):
        payload = {
            'sku': 'TEST-SKU',
            'marketplaceId': 'EBAY-AU',
            'format': 'FIXED_PRICE',
            'availableQuantity': 10,
            'pricingSummary': {'price': {'value': '19.99', 'currency': 'USD'}}
        }
        response = self.ebay_api.create_offer(payload)
        self.assertTrue('offerId' in response)

    def test_publish_offer(self):
        offer_id = 'TEST-OFFER-ID'
        response = self.ebay_api.publish_offer(offer_id)
        self.assertEqual(response['status'], 'PUBLISHED')

    def test_update_inventory_quantity(self):
        sku = 'TEST-SKU'
        new_qty = 15
        response = self.ebay_api.update_inventory_quantity(sku, new_qty)
        self.assertTrue(response)

if __name__ == '__main__':
    unittest.main()