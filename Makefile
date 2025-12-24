up:
	docker compose up --build

down:
	docker compose down -v

test:
	docker compose run api pytest

