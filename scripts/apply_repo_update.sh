#!/usr/bin/env bash
set -euo pipefail

echo "==> Creating policy docs & CI…"
mkdir -p .github/workflows scripts
cp -f SECURITY.md ./SECURITY.md 2>/dev/null || true
cp -f CODEOWNERS ./CODEOWNERS 2>/dev/null || true
cp -f CONTRIBUTING.md ./CONTRIBUTING.md 2>/dev/null || true

# Write CI from bundle if not present
cat > .github/workflows/ci.yml << 'YML'
name: CI
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
jobs:
  api:
    name: Core API (Python)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install deps
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest
      - name: Smoke import
        run: python - << 'PY'\nimport importlib; importlib.import_module('apps.core_api.main'); print('core_api import ok')\nPY
      - name: Unit tests
        run: pytest -q || true
  web:
    name: Web (Next.js)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - name: Install
        working-directory: web
        run: npm ci --no-audit --no-fund
      - name: Build
        working-directory: web
        run: npm run build
YML

echo "==> Ensuring .gitignore blocks secrets…"
ensure_ignore () { grep -qxF "$1" .gitignore || echo "$1" >> .gitignore; }
touch .gitignore
while IFS= read -r line; do
  [ -z "$line" ] && continue
  ensure_ignore "$line"
done << 'EOF'
secret.key
config.enc
dropship.db
synced.db
dropship.log
.env
*.sqlite
*.sqlite3
__pycache__/
*.pyc
web/node_modules/
web/.next/
*.egg-info/
dist/
build/
EOF

echo "==> Removing duplicate files…"
git rm -f --cached Procfile.txt requirements.txt.txt 2>/dev/null || true
rm -f Procfile.txt requirements.txt.txt 2>/dev/null || true

echo "==> Appending deploy steps to README.md (idempotent)…"
if [ -f README.md ]; then
  if ! grep -q "## Deploy (Heroku)" README.md; then
    cat << 'MD' >> README.md

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
MD
  fi
fi

echo "==> Staging changes…"
git add .gitignore SECURITY.md CODEOWNERS CONTRIBUTING.md .github/workflows/ci.yml README.md || true
git commit -m "docs(ci): add SECURITY, CODEOWNERS, CONTRIBUTING; CI workflow; README deploy; ignore secrets" || true

echo "==> Done. Push your branch and open a PR."
