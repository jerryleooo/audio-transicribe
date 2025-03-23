#!/bin/bash
set -e

# Print environment variables for debugging
echo "Environment variables:"
echo "FLASK_APP: $FLASK_APP"
echo "FLASK_ENV: $FLASK_ENV"
echo "DATABASE_URL: $DATABASE_URL"

# Ensure directories exist and have correct permissions
mkdir -p /app/instance
mkdir -p /app/uploads
chmod -R 777 /app/instance
chmod -R 777 /app/uploads

# Start application
exec gunicorn \
    --workers=2 \
    --threads=2 \
    --timeout=300 \
    --keep-alive=5 \
    --max-requests=1000 \
    --max-requests-jitter=50 \
    --bind 0.0.0.0:8000 \
    "app.main:create_app()" 