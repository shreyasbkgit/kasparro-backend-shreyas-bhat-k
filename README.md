# Kasparro Backend & ETL Assignment

This project implements a production-style backend system with an end-to-end ETL pipeline and API service, designed as part of the Kasparro Backend & ETL Systems assignment.

---

## Data Sources

1. CoinPaprika API  
Endpoint: https://api.coinpaprika.com/v1/global  
Type: Global cryptocurrency market-level metrics  
Authentication: Not required (free-tier public endpoint)

2. CoinGecko CSV  
Type: Historical Bitcoin market data  
Format: CSV export  
Granularity: Time-series snapshots

---

## Architecture Overview

- Raw data is ingested separately per source into raw tables  
- Data is normalized into a unified observation schema  
- Semantic differences between sources are preserved  
- Incremental ingestion is supported via checkpoints  
- Backend API exposes normalized observations  
- PostgreSQL is used as the primary datastore  
- The entire system is fully Dockerized  

---

## ETL Pipeline

The ETL pipeline performs the following steps:

1. Initializes database schema on startup  
2. Ingests raw data from CoinPaprika API and CoinGecko CSV  
3. Transforms raw data into a unified observation model  
4. Stores normalized data for API access  

ETL execution is automatically triggered when the service starts.

---

## API Endpoints

GET /health  
Reports:
- Database connectivity status  
- Last ETL run timestamps per data source  

GET /data  
Returns normalized market observations.

Supports:
- Pagination using limit and offset  
- Filtering by source and symbol  

Includes response metadata:
- request_id  
- api_latency_ms  

---

## Running the System

Start all services:

make up

Once running, the API will be available at:

http://localhost:8000

Stop and clean up services:

make down

---

## Notes

- Environment variables are managed using a .env file (not committed to the repository)  
- Database and tables are created automatically on container startup  
- The system is designed to be easily extendable for additional data sources and analytics  

