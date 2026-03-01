# Retail Data Ingestion Pipeline
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white) ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

An automated ETL (Extract, Transform, Load) pipeline designed to process over **1 million rows** of retail transaction data from Excel into a PostgreSQL database using Docker.

---

## Architecture Overview
The system utilizes three primary containers connected via a dedicated bridge network:

* **PostgreSQL 15**: The relational data warehouse.
* **Python Feeder**: Custom-built image for high-speed data streaming.
* **pgAdmin 4**: Web-based administration and visualization.



---

## The Dockerfile Breakdown
We "Dockerized" the environment to ensure portability and consistency. Each instruction creates a layer in our final **702MB** image.

| Instruction | Purpose |
| :--- | :--- |
| `FROM python:3.13.10-slim` | Lightweight Linux base with Python pre-installed. |
| `WORKDIR /app` | Sets the internal container directory for all operations. |
| `COPY requirements.txt .` | Pulls in the library list (`pandas`, `sqlalchemy`, etc). |
| `RUN pip install ...` | Bakes the dependencies into the image layer. |
| **`COPY . .`** | **Critical:** Copies the script and the 50MB Excel dataset into the image. |
| `ENTRYPOINT` | Automates the execution of `onlinestore.py` on startup. |



---

##  Deployment Steps

### 1. Network Setup
Create a virtual bridge so containers can communicate using names instead of IPs.
```bash
docker network create pipeline-network
```

### 2: Database Launch
Start the PostgreSQL instance with custom credentials.
```bash
docker run -d \
  --name postgres-db \
  --network pipeline-network \
  -e POSTGRES_USER=root \
  -e POSTGRES_PASSWORD=root \
  -e POSTGRES_DB=online_retail \
  -p 5432:5432 \
  postgres:15
```

### 3: Build & Run Ingestion
Build the custom image and run the data feeder.
```bash
docker build -t feeder-image .

# Run the ingestion script
docker run -it --rm --network pipeline-network feeder-image \
  --pg_host postgres-db \
  --pg_user root \
  --pg_pass root \
  --pg_db online_retail
```

### 4: Verification (pgAdmin)
Launch the GUI to inspect the data at http://localhost:8085.
```bash
docker run -d \
  --name pgadmin \
  --network pipeline-network \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8085:80 \
  dpage/pgadmin4




