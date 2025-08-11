# Dropship Automator – Multi-Service Scaffold

This scaffold adds a **core FastAPI service**, a **Redis/RQ worker**, and a **minimal Next.js frontend**, plus a local `docker-compose.yml` for development.

> It ships in **simulation mode by default**. Swap in real eBay/Ali calls later. Your existing Tk app can continue to run separately.

## Quick start (Docker)

```bash
cp .env.example .env
# Edit .env with your IDs / secrets (or leave simulation defaults)
docker compose up --build
```

Services:
- core_api: http://localhost:8000
- frontend: http://localhost:3000
- redis: redis://localhost:6379

## Endpoints (core_api)
- `GET /health` → `{"ok": true}`
- `POST /import` → body `{ "ali_id": "12345", "title": "...", "attrs": {..} }`
- `POST /map-category` → body `{ "title": "...", "description": "...", "attrs": {...}, "marketplace": "EBAY-AU" }`
- `GET /affiliate/link?ali_id=12345` → simulated affiliate link (no eBay listing injection)

> The `/map-category` endpoint includes a rule + alias mapping for demo (ALI_TO_EBAY). Later, enable embeddings or eBay Taxonomy API calls.

## GitHub project automation

Run `scripts/setup_github.sh` with the **GitHub CLI (`gh`)** installed and authenticated. It creates:
- A project board with columns
- Milestones
- Labels (area/*, track/*, priority/*)
- Issues for the 12-week roadmap

```bash
bash scripts/setup_github.sh c0mp4nionway Global-Marketplace-Bridge
```

## Notes
- Keep secrets out of source; use `.env` (and Heroku Config Vars in cloud).
- Consider migrating DB to Postgres in cloud; SQLite is fine locally.
- This scaffold is intentionally minimal and safe to expand.
