# TRM-OS API Production Dockerfile
# Python 3.11 slim base image for optimal size and security
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PORT=8000

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN groupadd -r trm && useradd -r -g trm trm

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY trm_api/ ./trm_api/
COPY scripts/ ./scripts/
COPY migrations/ ./migrations/

# Copy configuration files
COPY pytest.ini .
COPY docker-compose.yml .

# Make startup scripts executable
RUN chmod +x /app/scripts/start.sh /app/scripts/start.py

# Create necessary directories
RUN mkdir -p /app/logs /app/data

# Change ownership to non-root user
RUN chown -R trm:trm /app

# Switch to non-root user
USER trm

# Health check - simplified for Railway deployment
HEALTHCHECK --interval=30s --timeout=30s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose port
EXPOSE 8000

# Use Python startup script for maximum compatibility
CMD ["python", "/app/scripts/start.py"] 