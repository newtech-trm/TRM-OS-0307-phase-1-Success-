#!/bin/bash

# TRM-OS Production Startup Script
# Handles PORT environment variable for Railway deployment

# Set default port if PORT is not set or empty
if [ -z "$PORT" ]; then
    PORT=8000
fi

echo "Starting TRM-OS API on port $PORT"
echo "Environment: $(env | grep -E '^(PORT|PYTHONPATH|NEO4J_|DATABASE_)' | sort)"

# Start uvicorn with proper port
exec python -m uvicorn trm_api.main:app \
    --host 0.0.0.0 \
    --port "$PORT" \
    --workers 4 \
    --log-level info \
    --access-log 