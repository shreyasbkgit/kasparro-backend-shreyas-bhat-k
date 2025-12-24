---
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/97f6b8ed-4613-4c16-842a-f2a806cf6887" />
---


# Kasparro Backend – ETL & API System

This project implements a **Dockerized ETL + API backend** for cryptocurrency market data as part of the Kasparro backend assignment.
The system supports **scheduled ETL ingestion**, **manual ETL execution**, **persistent storage**, and **public API access**, and is fully deployed on **AWS EC2**.


---

## 📦 What This System Does

### Data Sources

The ETL pipeline ingests and consolidates cryptocurrency market data from **three distinct data sources**:

* **CoinGecko (BTC historical data)**
  Historical Bitcoin price and market data ingested from CSV files.

* **CoinGecko (ETH historical data)**
  Historical Ethereum price and market data ingested from CSV files.

* **CoinPaprika (Global market snapshot)**
  Real-time global cryptocurrency market data ingested via REST API.

Each source is:

* Tracked independently
* Incrementally ingested
* Persisted with source attribution for filtering and analytics


## 🚀 Deployed Backend (AWS)

**Public API Base URL (AWS EC2):**

```text
http://13.204.43.83:8000
```

### Available Endpoints

* **Health Check**

  ```text
  /health
  ```

* **Ingested Market Data**

  ```text
  /data
  ```

* **ETL Run Statistics**

  ```text
  /stats
  ```

---

## 📦 What This System Does

### Data Sources

* **CoinGecko** – BTC, ETH historical market data (CSV-based ingestion)
* **CoinPaprika** – Global crypto market snapshot (REST API)

### ETL Features

* Incremental ingestion
* Persistent checkpoints
* ETL run tracking (success / failure / duration / record count)
* Recovery-safe (ETL can be re-run after restart)
* Scheduled ETL using **cron inside Docker**

### API Features

* Health monitoring (`/health`)
* Filtered & paginated market data access (`/data`)
* ETL history & metrics (`/stats`)
* PostgreSQL-backed persistence

---

## 🐳 Dockerized Architecture

The system runs using **Docker Compose** with two services:

* **api** – FastAPI + ETL engine + cron scheduler
* **postgres** – PostgreSQL database with persistent volume

Everything starts automatically via Docker.

---

## 🐳 Docker Compose Configuration

Download the following `docker-compose.yml` file and run the system using Docker Compose.

```yaml
services:
  postgres:
    image: postgres:16
    container_name: kasparro-postgres
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  api:
    image: shreyasdocmysqli/kasparro-backend:latest
    container_name: kasparro-api
    depends_on:
      postgres:
        condition: service_healthy
    env_file:
      - .env
    ports:
      - "8000:8000"

volumes:
  pgdata:
```

---

### Expected `.env` File

Create a `.env` file in the same directory as `docker-compose.yml`.

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres

DATABASE_URL=postgresql+psycopg2://postgres:postgres@postgres:5432/postgres
```

---

## 🛠️ How to Run Locally (Same as AWS)

### Prerequisites

* Docker
* Docker Compose

### Start the System

```bash
docker-compose up --build -d
```

### Verify

```bash
docker ps
```

---

## 🔁 Running ETL Manually

ETL also runs on a **cron schedule**, but can be triggered manually:

```bash
docker-compose exec api python services/run_etl.py
```

After running ETL, verify:

```bash
curl http://localhost:8000/stats
curl http://localhost:8000/data
```

---

## 🔍 Data Access: Filtering, Pagination & Querying

The `/data` endpoint supports **server-side filtering and pagination**, enabling efficient querying of large historical datasets.

### Endpoint

```http
GET /data
```

---

### Pagination Parameters

| Parameter   | Type | Default | Description           |
| ----------- | ---- | ------- | --------------------- |
| `page`      | int  | `1`     | Page number (1-based) |
| `page_size` | int  | `50`    | Records per page      |

```bash
curl "http://localhost:8000/data?page=2&page_size=25"
```

---

### Source Filtering

| Parameter | Type   | Description                |
| --------- | ------ | -------------------------- |
| `source`  | string | Filter by ingestion source |

Valid values:

* `coingecko`
* `coinpaprika`

```bash
curl "http://localhost:8000/data?source=coingecko"
```

---

### Asset Filtering

| Parameter    | Type   | Description                             |
| ------------ | ------ | --------------------------------------- |
| `symbol`     | string | Filter by crypto symbol (e.g. BTC, ETH) |
| `asset_name` | string | Case-insensitive asset name filter      |

```bash
curl "http://localhost:8000/data?symbol=BTC"
```

---

### Date Range Filtering

| Parameter    | Type   | Format       | Description            |
| ------------ | ------ | ------------ | ---------------------- |
| `start_date` | string | `YYYY-MM-DD` | Start date (inclusive) |
| `end_date`   | string | `YYYY-MM-DD` | End date (inclusive)   |

```bash
curl "http://localhost:8000/data?start_date=2023-01-01&end_date=2023-06-30"
```

---

### Combined Filters

```bash
curl "http://localhost:8000/data?source=coingecko&symbol=BTC&page=1&page_size=10"
```

---

## 📊 ETL Statistics Endpoint

### Endpoint

```http
GET /stats
```

### Metrics Provided

* Execution timestamp
* Status (`success` / `failure`)
* Records ingested
* Execution duration
* Error message (if applicable)

---

## 🧪 Automated Tests

The project includes a full automated test suite using **pytest**.

### Covered Areas

* API health endpoint
* Pagination correctness
* Source-based filtering
* ETL side effects
* ETL statistics
* Database connectivity

```bash
pytest tests/
```

---

## 🧠 Design Guarantees

* Incremental & idempotent ETL
* Restart-safe ingestion
* Pagination enforced at database level
* No full-table API scans
* Stateless API layer
* Production-safe defaults

---

**Built with clarity, correctness, and production discipline.**

---




  


