# Real-Time Blood Bank Supply Chain Pipeline

Blood banks must continuously monitor donations, hospital requests, inventory levels, and emergency shortages.

This project simulates blood bank operations using modern big data technologies.

The pipeline continuously generates blood bank events, streams them through Apache Kafka, processes them using Spark Structured Streaming, stores them in Amazon RDS MySQL, and visualizes live insights with Streamlit.

---

## Project Overview

This project demonstrates an end-to-end real-time data engineering pipeline for blood bank supply chain management.

```text
Faker Data Generator
        │
        ▼
Python Kafka Producer
        │
        ▼
Apache Kafka
        │
        ▼
Spark Structured Streaming
        │
        ▼
Amazon RDS MySQL
        │
        ▼
Streamlit Dashboard
```

The system continuously generates realistic blood bank events such as donations, requests, dispatches, and inventory updates. These events are processed in real time and stored in Amazon RDS MySQL, while the Streamlit dashboard provides live operational insights and analytics.

---

## Features

- Real-time blood bank event generation using Faker
- Apache Kafka-based event streaming
- Spark Structured Streaming for real-time processing
- Amazon RDS MySQL integration
- Interactive Streamlit dashboard
- Live blood inventory monitoring
- Blood group distribution analysis
- Hospital-wise analytics
- City-wise event analysis
- Daily event trends
- Inventory availability tracking
- Interactive Plotly visualizations
- CSV export functionality

---

## Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Application Development |
| Faker | Synthetic Data Generation |
| Apache Kafka | Real-Time Data Streaming |
| Apache Spark Structured Streaming | Stream Processing |
| Amazon RDS MySQL | Cloud Database |
| Streamlit | Interactive Dashboard |
| Plotly | Data Visualization |
| Pandas | Data Analysis |
| Git & GitHub | Version Control |

---

## Project Architecture

```text
                 +----------------------+
                 |   Faker Generator    |
                 +----------+-----------+
                            |
                            ▼
                 +----------------------+
                 |  Python Producer     |
                 +----------+-----------+
                            |
                            ▼
                 +----------------------+
                 |   Apache Kafka       |
                 |       Topic          |
                 +----------+-----------+
                            |
                            ▼
                 +----------------------+
                 | Spark Structured     |
                 | Streaming            |
                 +----------+-----------+
                            |
                Data Validation &
                 Transformation
                            |
                            ▼
                 +----------------------+
                 | Amazon RDS MySQL     |
                 +----------+-----------+
                            |
                            ▼
                 +----------------------+
                 | Streamlit Dashboard  |
                 |    + Plotly Charts   |
                 +----------------------+
```

---

## Project Structure

```text
Real-time-blood-bank-supply-chain-pipeline/

│
├── dashboard/
│   ├── app.py
│   ├── db.py
│   └── style.css
│
├── producer/
│   ├── producer.py
│   ├── faker_data.py
│   ├── config.py
│   └── schemas.py
│
├── spark/
│   ├── consumer.py
│   ├── mysql_writer.py
│   ├── transformations.py
│   ├── schema.py
│   └── config.py
│
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
└── assets/
    ├── dashboard1.png
    ├── dashboard2.png
    ├── architecture.png
    └── pipeline.png
```

---

## Data Pipeline

### 1. Data Generation

The Python producer generates realistic blood bank events using the Faker library.

Generated events include:

- Blood Unit ID
- Donor ID
- Donor Name
- Blood Group
- Event Type
- Quantity
- Hospital Name
- City
- State
- Inventory Status
- Event Timestamp

---

### 2. Kafka Streaming

The generated events are published to an Apache Kafka topic.

```text
Python Producer
      │
      ▼
Kafka Topic
```

Apache Kafka acts as the messaging layer between the producer and Spark Streaming.

---

### 3. Spark Structured Streaming

Spark continuously consumes events from Kafka and performs:

- JSON Parsing
- Schema Validation
- Data Cleaning
- Data Transformation
- Database Storage

```text
Kafka
   │
   ▼
Spark Structured Streaming
   │
   ├── Parse JSON
   ├── Validate Schema
   ├── Transform Data
   └── Write to Amazon RDS
```

---

### 4. Amazon RDS MySQL

Processed records are stored in an Amazon RDS MySQL database.

The database acts as the central repository for all blood bank events and inventory information.

---

### 5. Streamlit Dashboard

The Streamlit dashboard connects to Amazon RDS MySQL and displays real-time analytics.

Dashboard includes:

- Total Events
- Blood Group Distribution
- Available Inventory
- Hospital-wise Analysis
- City-wise Analysis
- Daily Event Trends
- Latest Blood Bank Events
- Interactive Filters
- CSV Download

---

## Dashboard

### Main Dashboard

```text
assets/dashboard1.png
```

### Analytics Dashboard

```text
assets/dashboard2.png
```

---

## Prerequisites

Before running the project, ensure the following software is installed:

- Python 3.x
- Java
- Apache Kafka
- Apache Spark
- MySQL Client or MySQL Workbench
- Amazon RDS MySQL Database
- Git
- Streamlit

---

## Kafka Setup

Ensure that:

1. Apache Kafka is installed.
2. ZooKeeper is running.
3. Kafka Broker is running.
4. A Kafka topic has been created.
5. Producer can publish messages.
6. Spark Streaming can consume messages.

Data flow:

```text
Producer
    │
    ▼
Kafka Topic
    │
    ▼
Spark Structured Streaming
```

---

## Environment Variables

Database credentials are stored in a `.env` file.

Example:

```env
DB_HOST=your_rds_endpoint
DB_PORT=3306
DB_NAME=blood_bank
DB_USER=your_username
DB_PASSWORD=your_password

KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_TOPIC=blood_bank_topic
```

Sensitive credentials are never committed to GitHub.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/manthan026
/Real-time-blood-bank-supply-chain-pipeline.git
```

Navigate to the project:

```bash
cd Real-time-blood-bank-supply-chain-pipeline
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:

Linux / WSL

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file using `.env.example`.

---

## Running the Project

### Start ZooKeeper

```bash
zookeeper-server-start.sh config/zookeeper.properties
```

### Start Kafka

```bash
kafka-server-start.sh config/server.properties
```

### Run Producer

```bash
python producer/producer.py
```

### Run Spark Streaming

```bash
spark-submit spark/consumer.py
```

### Launch Dashboard

```bash
streamlit run dashboard/app.py
```

---

## Security

The following files are excluded from GitHub:

```text
.env
venv/
__pycache__/
checkpoints/
jars/
*.pem
```

Sensitive credentials are managed using environment variables and are never hardcoded.

---

## Future Improvements

- Docker deployment
- Kubernetes orchestration
- Apache Airflow scheduling
- AWS S3 integration
- Grafana monitoring
- Machine learning for blood demand prediction
- REST API
- Email notifications
- Authentication and role-based access control

---

## Author

**Manthan**

GitHub: https://github.com/manthan026


---

## License

This project is licensed for educational and portfolio purposes.