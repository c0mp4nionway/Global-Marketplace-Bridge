## Deploy (Heroku)

**Monorepo Procfile** is included at repo root. Two dynos:
- `web`: FastAPI core (`apps.core_api.main:app`)
- `worker`: RQ worker (`apps.worker.worker`)

### Steps
```bash
heroku create gmbridge-core --region eu
heroku buildpacks:set heroku/python -a gmbridge-core
heroku addons:create heroku-redis:mini -a gmbridge-core
heroku config:set SIMULATION=1 MARKETPLACE_ID=EBAY-AU NEXT_PUBLIC_API_BASE=https://gmbridge-core.herokuapp.com -a gmbridge-core
git push heroku main  # or your branch
heroku ps:scale web=1 worker=1 -a gmbridge-core
```

> For Docker deploys, use the provided `docker-compose.yml` locally and set `stack: container` for Heroku if you prefer containers.
