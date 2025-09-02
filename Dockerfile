# Use official Python runtime as base image
FROM python:3.12-slim

# Set working directory in container
WORKDIR /backend

# Copy requirements file first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

EXPOSE 8080

CMD sh -c 'uvicorn main:app --host 0.0.0.0 --port $PORT'