from dotenv import load_dotenv
import os

load_dotenv()

# ==========================================
# Kafka Configuration
# ==========================================

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")

# ==========================================
# Spark Configuration
# ==========================================

APP_NAME = "BloodBankStreaming"

CHECKPOINT_LOCATION = "checkpoints/blood-bank"

# ==========================================
# MySQL JDBC Driver
# ==========================================

MYSQL_JAR_PATH = (
    "/mnt/c/Users/RISHI/OneDrive/Desktop/project/"
    "Blood-bank-project/jars/mysql-connector-j-9.7.0/"
    "mysql-connector-j-9.7.0.jar"
)

# ==========================================
# Amazon RDS MySQL Configuration
# ==========================================

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")

MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")

# Existing table in RDS
MYSQL_TABLE = "blood_donations"

MYSQL_URL = (
    f"jdbc:mysql://{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    "?useSSL=false"
    "&allowPublicKeyRetrieval=true"
    "&serverTimezone=Asia/Kolkata&rewriteBatchedStatements=true"
)

# JDBC Driver Class
MYSQL_DRIVER = "com.mysql.cj.jdbc.Driver"