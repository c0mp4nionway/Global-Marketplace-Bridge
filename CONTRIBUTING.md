# Contributing

Thanks for contributing to **Global Marketplace Bridge (Dropship Automator)**!

## Ways to help
- Bug reports & minimal reproductions
- Feature proposals with user benefit and acceptance criteria
- Tests, docs, and refactors

## Development Setup
### Prereqs
- Python 3.11+
- Node 20+
- (Optional) Docker / Docker Compose

### Python (Core API)
```bash
python -m venv .venv && source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn apps.core_api.main:app --reload
# API at http://localhost:8000 (try /health)
```

### Web (Next.js)
```bash
cd web
npm ci
npm run dev
# Web at http://localhost:3000
# Ensure NEXT_PUBLIC_API_BASE points to your API (e.g., http://localhost:8000)
```

### Docker (All services)
```bash
docker compose up --build
# API: http://localhost:8000, Web: http://localhost:3000
```

## Coding standards
- Python: type hints where practical. Keep interfaces small & testable.
- Prefer FastAPI for API endpoints; avoid blocking I/O in request handlers.
- Frontend: Next.js + TypeScript, Tailwind, shadcn/radix where appropriate.
- No secrets in code. Use `.env` locally (never commit).

## Tests & CI
- Add or update tests for new behavior.
- CI runs lint/build/tests on PRs to `main`.
- Keep PRs focused; 200–400 lines per PR is a good target.

## Commit messages
- Use conventional style if possible: `feat:`, `fix:`, `chore:`, `docs:`, `test:`, `refactor:`

## Security
- See `SECURITY.md`. If you find a vulnerability, email the security inbox and avoid public issues.
