from tkinter import Tk, ttk, messagebox
from config.schema import ConfigSchema
from config.storage import load_config, save_config
from api.ebay import EbayAPI
from api.aliexpress import AliExpressAPI

class AppGUI(Tk):
    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg
        self.ebay_api = EbayAPI(cfg)
        self.ali_api = AliExpressAPI(cfg)
        self.title('Dropship Automator')
        self.geometry('800x600')
        self._build()

    def _build(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill='both', expand=True)

        # Configuration Frame
        config_frame = ttk.Frame(notebook)
        notebook.add(config_frame, text='Configuration')
        self._build_config_frame(config_frame)

        # Import Frame
        import_frame = ttk.Frame(notebook)
        notebook.add(import_frame, text='Import')
        self._build_import_frame(import_frame)

        # Sync Frame
        sync_frame = ttk.Frame(notebook)
        notebook.add(sync_frame, text='Sync')
        self._build_sync_frame(sync_frame)

        # Analytics Frame
        analytics_frame = ttk.Frame(notebook)
        notebook.add(analytics_frame, text='Analytics')
        self._build_analytics_frame(analytics_frame)

    def _build_config_frame(self, frame):
        ttk.Label(frame, text='eBay Token:').grid(column=0, row=0, padx=8, pady=8)
        self.ebay_token_var = ttk.StringVar(value=self.cfg['ebay']['token'])
        ttk.Entry(frame, textvariable=self.ebay_token_var, width=60).grid(column=1, row=0, padx=8, pady=8)
        ttk.Button(frame, text='Save Config', command=self.save_config).grid(column=1, row=1, padx=8, pady=10)

    def _build_import_frame(self, frame):
        ttk.Label(frame, text='AliExpress ID/URL:').grid(column=0, row=0, padx=8, pady=8)
        self.ali_entry = ttk.Entry(frame, width=50)
        self.ali_entry.grid(column=1, row=0, padx=8, pady=8)
        ttk.Button(frame, text='Import Single', command=self.import_single).grid(column=1, row=1, padx=8, pady=8)

    def _build_sync_frame(self, frame):
        ttk.Button(frame, text='Sync Now', command=self.sync_now).grid(column=0, row=0, padx=8, pady=8)

    def _build_analytics_frame(self, frame):
        ttk.Button(frame, text='Show Analytics', command=self.show_analytics).grid(column=0, row=0, padx=8, pady=8)

    def save_config(self):
        self.cfg['ebay']['token'] = self.ebay_token_var.get().strip()
        save_config(self.cfg)
        messagebox.showinfo('Saved', 'Configuration saved successfully.')

    def import_single(self):
        ali_id = self.ali_entry.get().strip()
        if not ali_id:
            messagebox.showwarning('Input Error', 'Please enter a valid AliExpress ID or URL.')
            return
        # Logic to import single product goes here

    def sync_now(self):
        # Logic to sync products goes here
        messagebox.showinfo('Sync', 'Sync completed successfully.')

    def show_analytics(self):
        # Logic to show analytics goes here
        messagebox.showinfo('Analytics', 'Displaying analytics...')

if __name__ == '__main__':
    config = load_config()
    app = AppGUI(config)
    app.mainloop()