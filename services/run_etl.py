from core.wait_for_db import wait_for_db
from core.init_db import init_db
from ingestion.coinpaprika import ingest_coinpaprika
from ingestion.csv_loader import ingest_csv
from services.transform import transform_coinpaprika, transform_csv

def run_etl():
    wait_for_db()
    init_db()

    ingest_coinpaprika()
    ingest_csv()

    transform_coinpaprika()
    transform_csv()

if __name__ == "__main__":
    run_etl()

