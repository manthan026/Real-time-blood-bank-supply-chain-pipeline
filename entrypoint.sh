#!/bin/bash
set -e

echo "=================================================="
echo " Starting Embedded MySQL Server in Container..."
echo "=================================================="

# Ensure directories exist and have proper permissions
mkdir -p /var/run/mysqld /var/lib/mysql
chown -R mysql:mysql /var/run/mysqld /var/lib/mysql
chmod 777 /var/run/mysqld

# Initialize MySQL system data directory if missing
if [ ! -d "/var/lib/mysql/mysql" ]; then
    echo ">> Initializing MySQL system data directory..."
    mysql_install_db --user=mysql --datadir=/var/lib/mysql > /dev/null 2>&1 || true
fi

# Start MySQL daemon in background
echo ">> Starting mysqld daemon on 127.0.0.1:3306..."
mysqld --user=mysql --datadir=/var/lib/mysql --bind-address=127.0.0.1 --port=3306 &
MYSQL_PID=$!

# Wait for MySQL to become ready
echo ">> Waiting for MySQL to accept connections..."
for i in {1..30}; do
    if mysqladmin ping --host=127.0.0.1 --silent 2>/dev/null; then
        echo ">> MySQL is healthy and ready!"
        break
    fi
    sleep 1
done

# Initialize database, user, and schema
echo ">> Initializing database 'blood_bank' and table schema..."
mysql -h 127.0.0.1 -u root <<'EOF' 2>/dev/null || true
CREATE DATABASE IF NOT EXISTS blood_bank;
CREATE USER IF NOT EXISTS 'blood_user'@'localhost' IDENTIFIED BY 'blood_pass_123';
CREATE USER IF NOT EXISTS 'blood_user'@'127.0.0.1' IDENTIFIED BY 'blood_pass_123';
CREATE USER IF NOT EXISTS 'blood_user'@'%' IDENTIFIED BY 'blood_pass_123';
GRANT ALL PRIVILEGES ON blood_bank.* TO 'blood_user'@'localhost';
GRANT ALL PRIVILEGES ON blood_bank.* TO 'blood_user'@'127.0.0.1';
GRANT ALL PRIVILEGES ON blood_bank.* TO 'blood_user'@'%';
FLUSH PRIVILEGES;
USE blood_bank;
CREATE TABLE IF NOT EXISTS blood_donations (
    event_id VARCHAR(100) PRIMARY KEY,
    event_timestamp VARCHAR(50),
    blood_bank VARCHAR(150),
    city VARCHAR(100),
    state VARCHAR(100),
    event_type VARCHAR(50),
    donor_id VARCHAR(50),
    donor_name VARCHAR(150),
    age INT,
    gender VARCHAR(20),
    blood_group VARCHAR(10),
    component VARCHAR(50),
    units INT,
    status VARCHAR(50),
    request_id VARCHAR(50),
    hospital VARCHAR(150),
    priority VARCHAR(50),
    screening_id VARCHAR(50),
    screening_status VARCHAR(50),
    transfer_id VARCHAR(50),
    destination_bank VARCHAR(150),
    dispatch_id VARCHAR(50),
    inventory_id VARCHAR(50),
    available_units INT,
    expiry_id VARCHAR(50),
    expired_units INT,
    expiry_date VARCHAR(50),
    alert_id VARCHAR(50),
    alert_level VARCHAR(50),
    message TEXT,
    processed_time VARCHAR(50),
    event_date VARCHAR(50),
    event_hour INT
);
EOF
echo ">> MySQL database and table schema initialized successfully!"

# Set environment variables for the Python dashboard (fallback to local container MySQL)
export MYSQL_HOST="${MYSQL_HOST:-127.0.0.1}"
export MYSQL_PORT="${MYSQL_PORT:-3306}"
export MYSQL_DATABASE="${MYSQL_DATABASE:-blood_bank}"
export MYSQL_USER="${MYSQL_USER:-blood_user}"
export MYSQL_PASSWORD="${MYSQL_PASSWORD:-blood_pass_123}"

echo "=================================================="
echo " Launching Streamlit Dashboard on port ${PORT:-8501}..."
echo "=================================================="

# Run Streamlit in the foreground
exec streamlit run streamlit_app.py \
    --server.port="${PORT:-8501}" \
    --server.address="0.0.0.0" \
    --server.headless=true \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false \
    --browser.gatherUsageStats=false
