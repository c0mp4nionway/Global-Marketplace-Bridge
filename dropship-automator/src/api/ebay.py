class EbayAPI:
    def __init__(self, cfg):
        self.client_id = cfg['ebay']['client_id']
        self.client_secret = cfg['ebay']['client_secret']
        self.token = cfg.get('ebay', {}).get('token')
        self.use_sandbox = cfg['ebay'].get('use_sandbox', True)
        self.base_url = 'https://api.sandbox.ebay.com' if self.use_sandbox else 'https://api.ebay.com'
        self.token_url = f'{self.base_url}/identity/v1/oauth2/token'
        self.api_version = 'v1'

    def _get_access_token(self):
        if self.token and not self._is_token_expired():
            return self.token
        
        response = requests.post(
            self.token_url,
            auth=(self.client_id, self.client_secret),
            data={'grant_type': 'client_credentials'},
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        response.raise_for_status()
        token_data = response.json()
        self.token = token_data['access_token']
        self._save_token()
        return self.token

    def _is_token_expired(self):
        # Implement token expiration check logic
        return False

    def _save_token(self):
        # Implement token saving logic to persistent storage
        pass

    def create_inventory_item(self, sku: str, payload: dict):
        token = self._get_access_token()
        url = f'{self.base_url}/sell/inventory/v1/inventory_item/{sku}'
        headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
        response = requests.put(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()

    def create_offer(self, payload: dict):
        token = self._get_access_token()
        url = f'{self.base_url}/sell/inventory/v1/inventory_item/{payload["sku"]}/offer'
        headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()

    def publish_offer(self, offer_id: str):
        token = self._get_access_token()
        url = f'{self.base_url}/sell/inventory/v1/inventory_item/{offer_id}/offer'
        headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def update_inventory_quantity(self, sku: str, qty: int):
        token = self._get_access_token()
        url = f'{self.base_url}/sell/inventory/v1/inventory_item/{sku}'
        headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
        payload = {'availability': {'shipToLocationAvailability': {'quantity': qty}}}
        response = requests.patch(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()

    def get_orders(self):
        token = self._get_access_token()
        url = f'{self.base_url}/sell/orders/v1/order'
        headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()