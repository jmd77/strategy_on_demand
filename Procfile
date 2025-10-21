web: gunicorn src.app:app -k uvicorn.workers.UvicornWorker -b 0.0.0.0:${PORT:-8000} --timeout 120
