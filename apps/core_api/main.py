import os
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from dotenv import load_dotenv
import urllib.parse as urlparse

load_dotenv()

SIMULATION = os.getenv("SIMULATION", "true").lower() == "true"
MARKUP_PERCENT = float(os.getenv("MARKUP_PERCENT", "30.0"))
MARKETPLACE_ID = os.getenv("MARKETPLACE_ID", "EBAY-AU")
AFFILIATE_ENABLED = os.getenv("AFFILIATE_ENABLED", "true").lower() == "true"
ALI_AFF_TRACKING_ID = os.getenv("ALI_AFF_TRACKING_ID", "")
ALI_AFF_SUB_ID = os.getenv("ALI_AFF_SUB_ID", "")

ALI_TO_EBAY = {
    "Phones & Telecommunications": "15032",
    "Computer & Office": "58058",
    "Consumer Electronics": "293",
    "Women's Clothing": "11450",
    "Home & Garden": "11700",
}

app = FastAPI(title="Dropship Core API", version="0.1.0")

class ImportBody(BaseModel):
    ali_id: str
    title: Optional[str] = None
    attrs: Optional[Dict[str, Any]] = None

class MapBody(BaseModel):
    title: str
    description: Optional[str] = None
    attrs: Optional[Dict[str, Any]] = None
    marketplace: str = "EBAY-AU"

@app.get("/health")
def health():
    return {"ok": True, "simulation": SIMULATION}

@app.get("/affiliate/link")
def affiliate_link(ali_id: str = Query(..., description="AliExpress product id")):
    base_url = f"https://www.aliexpress.com/item/{ali_id}.html"
    if not AFFILIATE_ENABLED:
        return {"ali_id": ali_id, "link": base_url, "affiliate": False}

    params = {"dl": base_url}
    if ALI_AFF_TRACKING_ID:
        params["aff_pid"] = ALI_AFF_TRACKING_ID
    if ALI_AFF_SUB_ID:
        params["sub"] = ALI_AFF_SUB_ID

    link = "https://s.click.aliexpress.com/deep_link?" + urlparse.urlencode(params)
    return {"ali_id": ali_id, "link": link, "affiliate": True}

@app.post("/map-category")
def map_category(body: MapBody):
    # Minimal rule mapping: pick from attributes/title keywords; fallback to alias map
    title = (body.title or "").lower()
    attrs = body.attrs or {}
    hints = [attrs.get("category"), attrs.get("ali_first_level")]

    if "case" in title or "phone" in title:
        return {"categoryId": ALI_TO_EBAY["Phones & Telecommunications"], "confidence": 0.85, "source": "rule"}
    if "laptop" in title or "keyboard" in title:
        return {"categoryId": ALI_TO_EBAY["Computer & Office"], "confidence": 0.75, "source": "rule"}
    for h in hints:
        if not h:
            continue
        if h in ALI_TO_EBAY:
            return {"categoryId": ALI_TO_EBAY[h], "confidence": 0.7, "source": "alias"}

    # Fallback
    return {"categoryId": "99", "confidence": 0.2, "source": "fallback"}

@app.post("/import")
def import_product(body: ImportBody):
    # Simulate listing pipeline (Inventory->Offer->Publish) and return an offer id
    if SIMULATION:
        offer_id = f"SIM-OFFER-{body.ali_id}"
        return {
            "ok": True,
            "offerId": offer_id,
            "marketplaceId": MARKETPLACE_ID,
            "markup_percent": MARKUP_PERCENT,
        }
    raise HTTPException(status_code=501, detail="Live mode not yet implemented here")
