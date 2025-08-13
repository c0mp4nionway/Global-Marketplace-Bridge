## Deploy (Heroku)

This monorepo uses a root **Procfile**:
- `web`: FastAPI core (`apps.core_api.main:app` via uvicorn)
- `worker`: RQ worker (`apps.worker.worker`)

### One-time setup
```bash
heroku create gmbridge-core --region eu
heroku buildpacks:set heroku/python -a gmbridge-core
heroku addons:create heroku-redis:mini -a gmbridge-core
heroku config:set SIMULATION=1 MARKETPLACE_ID=EBAY-AU NEXT_PUBLIC_API_BASE=https://gmbridge-core.herokuapp.com -a gmbridge-core
```

### Deploy
```bash
git push heroku main
heroku ps:scale web=1 worker=1 -a gmbridge-core
```

> For local development, use `docker compose up --build` (API on :8000, Web on :3000).
