# Host: 127.0.0.1
# Port: 8000

# API will run on http://127.0.0.1:8000
# API documentation (Swagger UI) will be at http://127.0.0.1:8000/docs
# API documentation (ReDoc) will be at http://127.0.0.1:8000/redoc

./venv/bin/uvicorn main:app --reload
