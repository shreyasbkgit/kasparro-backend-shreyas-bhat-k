.PHONY: up down build logs restart

up:
	docker compose up --build

down:
	docker compose down -v

build:
	docker compose build --no-cache

logs:
	docker compose logs -f

restart:
	docker compose down -v
	docker compose up --build

