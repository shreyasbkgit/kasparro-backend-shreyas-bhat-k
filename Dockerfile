FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y cron

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY cron/etl-cron /etc/cron.d/etl-cron
RUN chmod 0644 /etc/cron.d/etl-cron && crontab /etc/cron.d/etl-cron

RUN touch /var/log/etl.log

CMD cron && uvicorn api.main:app --host 0.0.0.0 --port 8000

