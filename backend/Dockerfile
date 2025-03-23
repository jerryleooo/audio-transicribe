FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y ffmpeg

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set entrypoint (shell form)
ENTRYPOINT ./docker-entrypoint.sh