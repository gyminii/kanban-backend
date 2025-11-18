FROM python:3.12-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Render assigns PORT dynamically
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}