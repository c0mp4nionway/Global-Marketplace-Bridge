# Monorepo Procfile for Heroku
# Web dyno runs FastAPI core_api
web: uvicorn apps.core_api.main:app --host 0.0.0.0 --port ${PORT}
# Worker dyno runs RQ worker
worker: python -m apps.worker.worker
