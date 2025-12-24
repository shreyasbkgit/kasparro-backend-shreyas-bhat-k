---
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/97f6b8ed-4613-4c16-842a-f2a806cf6887" />
---

Docker HUB image:https://hub.docker.com/r/shreyasdocmysqli/kasparro-backend

---

Git:https://github.com/shreyasbkgit/kasparro-backend-shreyas-bhat-k/

---
to run the process

docker-compose exec api python services/run_etl.py


---

# Kasparro Backend – ETL & API System

This project implements a **Dockerized ETL + API backend** for cryptocurrency market data as part of the Kasparro backend assignment.
The system supports **scheduled ETL ingestion**, **manual ETL execution**, **persistent storage**, and **public API access**, and is fully deployed on **AWS EC2**.

---

## 🚀 Deployed Backend (AWS)

**Public API Base URL (AWS EC2):**

```
http://13.204.43.83:8000
```

### Available Endpoints

* **Health Check**

  ```
  http://13.204.43.83:8000/health
  ```

* **Ingested Market Data**

  ```
  http://13.204.43.83:8000/data
  ```

* **ETL Run Statistics**

  ```
  http://13.204.43.83:8000/stats
  ```

> ✅ Deployment is live on AWS EC2 (bonus criteria satisfied)

---

## 📦 What This System Does

### Data Sources

* **CoinGecko** (BTC, ETH historical CSV ingestion)
* **CoinPaprika** (Global crypto market snapshot via API)

### ETL Features

* Incremental ingestion
* Persistent checkpoints
* ETL run tracking (`success`, `failure`, duration, record count)
* Recovery-safe (can re-run ETL after restart)
* Scheduled ETL using **cron inside Docker**

### API Features

* Health monitoring (`/health`)
* Paginated & filtered data access (`/data`)
* ETL history & metrics (`/stats`)
* PostgreSQL-backed persistence

---

## 🐳 Dockerized Architecture

The system runs using **Docker Compose** with two services:

* **api** – FastAPI + ETL + cron scheduler
* **postgres** – PostgreSQL database with persistent volume

Everything starts automatically via Docker.

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

## 🧪 Automated Tests

The project includes a full automated test suite using **pytest**.

### Covered Areas

* API health endpoint
* Data pagination
* Source-based filtering
* ETL side effects
* ETL statistics
* Database connectivity

### Run Tests

```bash
pytest tests/
```

✅ All tests pass successfully.

---

## ☁️ AWS Deployment Details

* **Platform:** AWS EC2 (Ubuntu)
* **Runtime:** Docker + Docker Compose
* **Public Access:** Port 8000 open for API
* **ETL Scheduling:** Cron inside API container
* **Logs:** Accessible via Docker logs
* **Database:** PostgreSQL with Docker volume

---

## 🔐 Evaluator: SSH Access & Self-Run Instructions

### SSH into EC2

```bash
ssh -i <your-key>.pem ubuntu@13.204.43.83
```

### Navigate to Project

```bash
cd kasparro-backend-shreyas-bhat-k
```

### Start Services

```bash
docker-compose up --build -d
```

### Trigger ETL (Optional)

```bash
docker-compose exec api python services/run_etl.py
```

### View Logs

```bash
docker-compose logs api
docker-compose logs postgres
```

---

## ✅ Assignment Checklist

✔ Docker image
✔ Docker Compose setup
✔ Automated ETL
✔ Public API endpoints
✔ AWS cloud deployment
✔ Cron-based scheduling
✔ Persistent storage
✔ Full test suite
✔ Live smoke test

---

## 🧠 Notes

* No external API authentication is required for this assignment.
* All secrets and configuration are handled via environment variables.
* Evaluators can verify everything **without modifying code**.

---

**Built with clarity, correctness, and production discipline.**

Here’s the **clean, polished Markdown version** exactly in the style you’re aiming for. You can paste this **as-is** into `README.md`.

---

**Built with clarity, correctness, and production discipline.**

## Docker Compose Configuration

Download the following `docker-compose.yml` file and run the service using Docker Compose.

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

### Expected `.env` file (place in the same directory)

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres

DATABASE_URL=postgresql+psycopg2://postgres:postgres@postgres:5432/postgres
```

### Build and Run

```bash
docker compose up --build
```




  


