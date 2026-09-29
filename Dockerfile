# ==============================================================================
# Production Dockerfile for Blood Bank Supply Chain Dashboard
# With embedded MySQL Server & Streamlit inside the same container
# ==============================================================================

FROM python:3.10-slim

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8501 \
    DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Install MariaDB (MySQL compatible) server, client, curl, and process utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    mariadb-server \
    mariadb-client \
    curl \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Convert entrypoint script line endings and make executable
RUN sed -i 's/\r$//' /app/entrypoint.sh && chmod +x /app/entrypoint.sh

# Expose ports: 8501 for Streamlit and 3306 for MySQL
EXPOSE 8501 3306

# Healthcheck to ensure the container is responsive
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8501}/_stcore/health || exit 1

# Start MySQL daemon and Streamlit via entrypoint
ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]
