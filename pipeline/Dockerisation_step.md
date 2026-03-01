Retail Data Ingestion Pipeline
An automated ETL (Extract, Transform, Load) pipeline designed to process over 1 million rows of retail transaction data from Excel into a PostgreSQL database using Docker.

🏗️ Architecture Diagram
The following diagram illustrates how the three containers interact within the isolated Docker network:

🛠️ Tech Stack
Language: Python 3.13.10-slim

Libraries: pandas, openpyxl, sqlalchemy, psycopg2-binary, tqdm

Infrastructure: Docker, Docker Networking

Database: PostgreSQL 15

Management: pgAdmin 4

📄 The Dockerfile (The "Blueprint")
We "Dockerized" the Python script by creating a custom image. This process packages the code, the environment, and the data into a single 702MB unit.

Dockerfile

# 1. Start with a lightweight Python base
FROM python:3.13.10-slim

# 2. Set internal working directory
WORKDIR /app

# 3. Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the script AND the 50MB Excel file into the image
COPY . .

# 5. Define how to run the script
ENTRYPOINT ["python", "onlinestore.py"]
🚀 Step-by-Step Setup
1. Network Configuration
Created a virtual bridge so containers can communicate using their names (e.g., postgres-db) instead of IP addresses.

Bash

docker network create pipeline-network
2. Database Deployment
Launched the PostgreSQL instance.

Bash

docker run -d \
  --name postgres-db \
  --network pipeline-network \
  -e POSTGRES_USER=root \
  -e POSTGRES_PASSWORD=root \
  -e POSTGRES_DB=online_retail \
  -p 5432:5432 \
  postgres:15
3. Build & Run Ingestion
Build the image:

Bash

docker build -t feeder-image .
Execute the pipeline:

Bash

docker run -it --rm --network pipeline-network feeder-image \
  --pg_host postgres-db \
  --pg_user root \
  --pg_pass root \
  --pg_db online_retail
Performance Note: The script successfully combined multiple Excel sheets and uploaded 1,067,371 rows to the retail_data table.

4. Verification (pgAdmin)
Launched the GUI to inspect the data.

Bash

docker run -d \
  --name pgadmin \
  --network pipeline-network \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8085:80 \
  dpage/pgadmin4
📊 SQL Analysis
Connect to http://localhost:8085 and run these in the Query Tool:

Check Total Rows:

SQL

SELECT count(*) FROM retail_data;
Find Top 5 Best Selling Items:

SQL

SELECT "Description", SUM("Quantity") as total_sold
FROM retail_data
GROUP BY "Description"
ORDER BY total_sold DESC
LIMIT 5;
🧹 Maintenance
Start Services: docker start postgres-db pgadmin

Stop Services: docker stop postgres-db pgadmin

Cleanup: docker system prune (to remove stopped containers and <none> images).
