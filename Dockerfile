FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "while ! nc -z db 5432; do sleep 1; done && \
     alembic upgrade head && \
     uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"]