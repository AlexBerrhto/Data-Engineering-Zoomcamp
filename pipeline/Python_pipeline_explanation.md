# 🛠️ Data Ingestion CLI (Advanced Version)

This version of the pipeline transforms a static script into a professional **Command Line Interface (CLI)** using the `Click` library. It allows for dynamic configuration of database credentials and ingestion parameters without modifying the source code.

---

## 🏗️ Technical Logic & Workflow

The script follows a structured ETL process to ensure data integrity and performance:

1.  **Connection Management**: Uses `SQLAlchemy` to create a dynamic engine based on CLI arguments.
2.  **Schema Enforcement**: 
    * Drops existing tables to prevent duplicate data conflicts.
    * Explicitly defines SQL data types (`BIGINT`, `TIMESTAMP`, `FLOAT(53)`) to ensure the database matches the source Excel format.
3.  **Data Aggregation**: Utilizes `pandas.ExcelFile` to iterate through and concatenate all sheets within the workbook into a single DataFrame.
4.  **Optimized Loading**: 
    * Cleans column names by converting them to lowercase and replacing spaces with underscores.
    * Uses a **Chunking Strategy** with `tqdm` progress bars to stream data in batches, preventing memory overflow.



---

## ❓ Why we use `Click`
`Click` (Command Line Interface Creation Kit) is a Python package for creating beautiful command line interfaces in a composable way.

### 1. Separation of Concerns
By using `@click.option`, we separate the **logic** (how to move data) from the **configuration** (where the data goes). 

**Example:**
* **Without Click:** You have to open the file and change `pg_pass = 'root'` to `'secret123'`.
* **With Click:** You simply type: 
    ```bash
    python onlinestore.py --pg_pass secret123
    ```

### 2. Built-in Documentation (`--help`)
`Click` automatically generates a help menu based on your code. This acts as "self-documenting" code for other developers.
* **Command:** `python onlinestore.py --help`
* **Result:** Displays all available flags, their default values, and descriptions.

### 3. Practical Usage Example
Imagine deploying this script across different environments (Local vs. Production):

| Environment | Command Execution |
| :--- | :--- |
| **Local Dev** | `python onlinestore.py --pg_host localhost --chunksize 1000` |
| **Cloud Prod** | `python onlinestore.py --pg_host 10.0.0.5 --pg_db prod_retail --chunksize 50000` |



---

## 🚀 Execution Guide

### Available Arguments
| Flag | Default | Description |
| :--- | :--- | :--- |
| `--file_name` | `online_retail_II.xlsx` | Path to the source file |
| `--pg_user` | `root` | Postgres username |
| `--pg_host` | `localhost` | Database host address |
| `--target_table`| `retail_data` | Name of the table in Postgres |
| `--chunksize` | `10000` | Number of rows to upload per batch |

### Running in Docker
When using this script inside your `feeder-image`, you can pass these flags directly to the `docker run` command:

```bash
docker run -it --rm --network pipeline-network feeder-image \
  --pg_host postgres-db \
  --pg_db online_store \
  --chunksize 25000
