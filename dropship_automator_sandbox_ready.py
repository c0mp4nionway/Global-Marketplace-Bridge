"""
Dropship Automator — Sandbox-ready, Config Wizard, OAuth2, Build script & Tests
Merged and extended from the Clean Full hybrid. Adds:
 - eBay sandbox OAuth2 client_credentials token fetch and storage (encrypted)
 - First-run config wizard for entering required credentials
 - PyInstaller build script generator (Windows .bat)
 - Unit test skeletons using unittest.mock

Security: This script stores client id / secret and tokens encrypted in config.enc using Fernet (secret.key).
Replace placeholder scopes and endpoints if eBay changes their API.
"""

import os
import json
import time
import logging
import threading
import requests
import sqlite3
from datetime import datetime
from functools import wraps
from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext, simpledialog
import csv
import re
import difflib
import schedule
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import base64
import unittest
from unittest import mock

# Paths
APP_DIR = os.path.dirname(__file__) or '.'
KEY_FILE = os.path.join(APP_DIR, 'secret.key')
CONFIG_FILE = os.path.join(APP_DIR, 'config.enc')
DB_FILE = os.path.join(APP_DIR, 'dropship.db')
LOG_FILE = os.path.join(APP_DIR, 'dropship.log')
BUILD_SCRIPT = os.path.join(APP_DIR, 'build_win_exe.bat')

# Logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger('dropship')

# Defaults
DEFAULTS = {
    'ali_app_key': '',
    'ali_app_secret': '',
    'ebay_client_id': '',
    'ebay_client_secret': '',
    'ebay_token': '',
    'ebay_token_expires': 0,
    'marketplace_id': 'EBAY-AU',
    'markup_percent': 30.0,
    'sync_interval_hours': 6,
    'max_retries': 3,
    'retry_backoff_seconds': 2,
    'use_sandbox': True,
}

# eBay OAuth scopes we'll request for sandbox (adjust as needed)
EBAY_SCOPES = [
    'https://api.ebay.com/oauth/api_scope/sell.inventory',
    'https://api.ebay.com/oauth/api_scope/sell.fulfillment',
    'https://api.ebay.com/oauth/api_scope/sell.account',
]

# --------------------- Encryption helpers ---------------------

def load_or_create_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, 'wb') as f:
            f.write(key)
    with open(KEY_FILE, 'rb') as f:
        return f.read()

FERNET_KEY = load_or_create_key()
FERNET = Fernet(FERNET_KEY)


def encrypt_config(obj: dict):
    raw = json.dumps(obj).encode('utf-8')
    return FERNET.encrypt(raw)


def decrypt_config(blob: bytes):
    return json.loads(FERNET.decrypt(blob).decode('utf-8'))


def save_config(cfg: dict):
    with open(CONFIG_FILE, 'wb') as f:
        f.write(encrypt_config(cfg))
    logger.info('Config saved (encrypted)')


def load_config():
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULTS.copy())
        return DEFAULTS.copy()
    try:
        with open(CONFIG_FILE, 'rb') as f:
            blob = f.read()
        cfg = decrypt_config(blob)
        merged = DEFAULTS.copy()
        merged.update(cfg)
        return merged
    except Exception as e:
        logger.exception('Failed to load config: %s', e)
        save_config(DEFAULTS.copy())
        return DEFAULTS.copy()

# --------------------- DB init ---------------------

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY AUTOINCREMENT, ali_product_id TEXT UNIQUE, title TEXT, ebay_item_id TEXT, price REAL, qty INTEGER, last_sync TIMESTAMP, raw TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS prices (sku TEXT PRIMARY KEY, price REAL)''')
    conn.commit()
    conn.close()

init_db()

# --------------------- retry decorator ---------------------

def retry(max_retries=3, backoff=2):
    def deco(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    logger.warning('Attempt %s failed for %s: %s', attempt, func.__name__, e)
                    if attempt >= max_retries:
                        logger.exception('Max retries reached for %s', func.__name__)
                        raise
                    time.sleep(backoff * attempt)
        return wrapper
    return deco

# --------------------- AliExpress API (simulated) ---------------------

class AliExpressAPI:
    def __init__(self, cfg):
        self.key = cfg.get('ali_app_key')
        self.secret = cfg.get('ali_app_secret')
        self.base = 'http://gw.api.taobao.com/router/rest'

    @retry(max_retries=3, backoff=2)
    def fetch_product(self, ali_id: str):
        logger.info('Fetching AliExpress product %s', ali_id)
        # Simulated product — replace with real API parsing
        return {
            'aliexpress_affiliate_productdetail_get_response': {
                'resp_result': {
                    'result': {
                        'products': [
                            {
                                'product_id': ali_id,
                                'subject': f'Sim Product {ali_id}',
                                'description': 'Sample description',
                                'target_sale_price': '9.99',
                                'total_avaliable_stock': '50',
                                'image_urls': 'https://via.placeholder.com/600',
                                'first_level_category_name': 'Phones & Telecommunications',
                                'brand_name': 'Demo',
                                'sku_infos': [{'sku_id': '1', 'color': 'Black'}],
                                'specs_module': {'Weight': '200g'}
                            }
                        ]
                    }
                }
            }
        }

# --------------------- eBay API (sandbox integration) ---------------------

class EbayAPI:
    def __init__(self, cfg):
        self.client_id = cfg.get('ebay_client_id')
        self.client_secret = cfg.get('ebay_client_secret')
        self.token = cfg.get('ebay_token')
        self.token_expires = cfg.get('ebay_token_expires', 0)
        self.use_sandbox = cfg.get('use_sandbox', True)
        self.base = 'https://api.sandbox.ebay.com' if self.use_sandbox else 'https://api.ebay.com'

    def needs_token(self):
        return not self.token or time.time() > (self.token_expires - 60)

    def obtain_app_token(self, scopes=None):
        scopes = scopes or EBAY_SCOPES
        token_url = f'{self.base}/identity/v1/oauth2/token'
        auth = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
        headers = {
            'Authorization': f'Basic {auth}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'grant_type': 'client_credentials',
            'scope': ' '.join(scopes)
        }
        logger.info('Requesting eBay app token (sandbox)')
        resp = requests.post(token_url, headers=headers, data=data, timeout=10)
        resp.raise_for_status()
        j = resp.json()
        self.token = j.get('access_token')
        expires_in = j.get('expires_in', 7200)
        self.token_expires = time.time() + int(expires_in)
        # persist token in config
        cfg = load_config()
        cfg['ebay_token'] = self.token
        cfg['ebay_token_expires'] = self.token_expires
        save_config(cfg)
        logger.info('Obtained eBay token, expires in %s seconds', expires_in)
        return self.token

    @retry(max_retries=3, backoff=2)
    def create_inventory_item(self, sku: str, payload: dict):
        url = f'{self.base}/sell/inventory/v1/inventory_item/{sku}'
        headers = {'Authorization': f'Bearer {self.token}', 'Content-Type': 'application/json'}
        resp = requests.put(url, headers=headers, json=payload, timeout=15)
        resp.raise_for_status()
        return resp.json()

    @retry(max_retries=3, backoff=2)
    def create_offer(self, payload: dict):
        url = f'{self.base}/sell/inventory/v1/offer'
        headers = {'Authorization': f'Bearer {self.token}', 'Content-Type': 'application/json'}
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        resp.raise_for_status()
        return resp.json()

    @retry(max_retries=3, backoff=2)
    def publish_offer(self, offer_id: str):
        url = f'{self.base}/sell/inventory/v1/offer/{offer_id}/publish'
        headers = {'Authorization': f'Bearer {self.token}'}
        resp = requests.post(url, headers=headers, timeout=15)
        resp.raise_for_status()
        return resp.json()

    @retry(max_retries=3, backoff=2)
    def update_inventory_quantity(self, sku: str, qty: int):
        url = f'{self.base}/sell/inventory/v1/inventory_item/{sku}'
        headers = {'Authorization': f'Bearer {self.token}', 'Content-Type': 'application/json'}
        payload = {'availability': {'shipToLocationAvailability': {'quantity': qty}}}
        resp = requests.put(url, headers=headers, json=payload, timeout=15)
        resp.raise_for_status()
        return resp.json()

    @retry(max_retries=3, backoff=2)
    def get_orders(self):
        url = f'{self.base}/sell/fulfillment/v1/order'
        headers = {'Authorization': f'Bearer {self.token}'}
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        return resp.json().get('orders', [])

# --------------------- Business logic (similar to clean full) ---------------------

def map_category(ali_category: str):
    if not ali_category:
        return None
    return ALI_TO_EBAY.get(ali_category)

class DropshipWorker:
    def __init__(self, cfg):
        self.cfg = cfg
        self.ali = AliExpressAPI(cfg)
        self.ebay = EbayAPI(cfg)
        self.sync_interval = int(cfg.get('sync_interval_hours', 6)) * 3600

    def import_single(self, ali_id: str, markup_percent: float = None):
        product_raw = self.ali.fetch_product(ali_id)
        prod = self._normalize_ali_product(product_raw)
        if markup_percent is None:
            markup_percent = self.cfg.get('markup_percent', 30.0)
        # ensure token
        if self.ebay.needs_token():
            self.ebay.obtain_app_token()
        return self._create_ebay_listing(prod, markup_percent)

    def _normalize_ali_product(self, raw):
        try:
            p = raw['aliexpress_affiliate_productdetail_get_response']['resp_result']['result']['products'][0]
        except Exception:
            raise ValueError('Unexpected AliExpress response')
        prod = {
            'id': p.get('product_id'),
            'title': p.get('subject'),
            'description': p.get('description'),
            'price': float(p.get('target_sale_price') or 0),
            'qty': int(p.get('total_avaliable_stock') or 0),
            'images': p.get('image_urls', '').split(';') if p.get('image_urls') else [],
            'variants': p.get('sku_infos', []),
            'category': p.get('first_level_category_name')
        }
        return prod

    def _create_ebay_listing(self, product: dict, markup_percent: float):
        title = (product.get('title') or '')[:80]
        price = round(product.get('price', 0) * (1 + markup_percent / 100.0), 2)
        qty = min(product.get('qty', 0), 999)
        sku = f"ALI-{product.get('id')}"

        # build inventory payload
        payload_inventory = {
            'availability': {'shipToLocationAvailability': {'quantity': qty}},
            'condition': 'NEW',
            'product': {
                'title': title,
                'description': product.get('description'),
                'imageUrls': product.get('images'),
                'aspects': {},
            }
        }
        inv = self.ebay.create_inventory_item(sku, payload_inventory)

        offer_payload = {
            'sku': sku,
            'marketplaceId': self.cfg.get('marketplace_id'),
            'format': 'FIXED_PRICE',
            'availableQuantity': qty,
            'pricingSummary': {'price': {'value': str(price), 'currency': 'USD'}}
        }
        offer = self.ebay.create_offer(offer_payload)
        offer_id = offer.get('offerId')
        pub = self.ebay.publish_offer(offer_id)

        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('INSERT OR REPLACE INTO products (ali_product_id, title, ebay_item_id, price, qty, last_sync, raw) VALUES (?, ?, ?, ?, ?, ?, ?)',
                  (product.get('id'), title, offer_id, price, qty, datetime.utcnow().isoformat(), json.dumps(product)))
        conn.commit()
        conn.close()
        logger.info('Created eBay listing %s for Ali %s', offer_id, product.get('id'))
        return offer_id

    # bulk, sync and other methods omitted for brevity — keep as in Clean Full

# -------------------- Image helper --------------------

def watermark_image_unique(image_url, sku):
    try:
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content)).convert('RGB')
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()
        draw.text((10, 10), '© Circle Group', fill='white', font=font)
        out = f'watermarked_{sku}_{int(time.time())}.jpg'
        img.save(out)
        logger.info('Saved watermark %s', out)
        return out
    except Exception as e:
        logger.warning('Watermark failed: %s', e)
        return image_url

# -------------------- Config wizard (first-run) --------------------

def run_config_wizard_if_needed(root, cfg):
    missing = []
    if not cfg.get('ebay_client_id'):
        missing.append('eBay App (Client) ID')
    if not cfg.get('ebay_client_secret'):
        missing.append('eBay Cert (Client Secret)')
    if not cfg.get('ali_app_key'):
        missing.append('AliExpress App Key')
    if missing:
        msg = 'Missing credentials: ' + ', '.join(missing) + '\n\nOpen config wizard to enter them now?'
        if messagebox.askyesno('Config required', msg):
            # simple dialog to gather values
            vid = simpledialog.askstring('eBay Client ID', 'Enter eBay App ID (Client ID):', parent=root)
            vsecret = simpledialog.askstring('eBay Client Secret', 'Enter eBay Cert (Client Secret):', parent=root)
            ali_key = simpledialog.askstring('AliExpress Key', 'Enter AliExpress App Key:', parent=root)
            ali_secret = simpledialog.askstring('AliExpress Secret', 'Enter AliExpress App Secret:', parent=root)
            if vid:
                cfg['ebay_client_id'] = vid.strip()
            if vsecret:
                cfg['ebay_client_secret'] = vsecret.strip()
            if ali_key:
                cfg['ali_app_key'] = ali_key.strip()
            if ali_secret:
                cfg['ali_app_secret'] = ali_secret.strip()
            save_config(cfg)
            messagebox.showinfo('Saved', 'Credentials saved (encrypted). Please restart the app.')

# -------------------- Build script creator --------------------

def ensure_build_script():
    content = f"""@echo off
REM Build Dropship Automator into a single executable using PyInstaller
pyinstaller --noconfirm --onefile --windowed --add-data "{KEY_FILE};." --add-data "{CONFIG_FILE};." dropship_automator_sandbox_ready.py
pause
"""
    try:
        with open(BUILD_SCRIPT, 'w', encoding='utf-8') as f:
            f.write(content)
        logger.info('Wrote build script to %s', BUILD_SCRIPT)
    except Exception as e:
        logger.warning('Failed to write build script: %s', e)

# -------------------- Unit tests (skeleton) --------------------

class TestEbayOAuth(unittest.TestCase):
    @mock.patch('requests.post')
    def test_obtain_app_token_success(self, mock_post):
        # simulate token response
        mock_post.return_value = mock.Mock(status_code=200)
        mock_post.return_value.json.return_value = {'access_token': 'TOKEN123', 'expires_in': 7200}
        cfg = load_config()
        cfg['ebay_client_id'] = 'DUMMY'
        cfg['ebay_client_secret'] = 'DUMMY'
        save_config(cfg)
        api = EbayAPI(cfg)
        token = api.obtain_app_token()
        self.assertEqual(token, 'TOKEN123')

# -------------------- Main (GUI) --------------------

def main():
    cfg = load_config()
    root = tk.Tk()
    root.withdraw()
    run_config_wizard_if_needed(root, cfg)
    root.destroy()

    # create build script
    ensure_build_script()

    # start main GUI app
    from tkinter import Tk
    app_root = Tk()
    from tkinter import messagebox
    class MinimalApp(app_root.__class__):
        pass
    # For brevity, reuse a simple window that informs user to run the clean-full app file.
    app_root.title('Dropship Automator - Sandbox Ready')
    w = tk.Label(app_root, text='Sandbox-ready utilities installed. Run Dropship Automator (clean full) to continue.', padx=20, pady=20)
    w.pack()
    app_root.mainloop()

if __name__ == '__main__':
    main()

"""Note: The real deployable GUI is in the cleaned 'Clean Full' script. This helper adds OAuth, build and tests.
Run `python dropship_automator_sandbox_ready.py` to create the build script and run the config wizard. 
To execute unit tests: python -m unittest this_file.py
"""
