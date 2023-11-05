setup-poetry:
	docker compose run --entrypoint "poetry init --name app --dependency fastapi --dependency uvicorn[standard]" app

setup:
	docker compose run --entrypoint "poetry install --no-root" app
	@make up

up:
	docker compose up -d

shell:
	docker compose exec app bash

mysql:
	docker compose exec db sh -c "PGPASSWORD=password password -U user"

build:
	docker compose up -d --build

down:
	docker compose down

restart: down up

migrate:
	docker compose exec app poetry run python -m api.migrate_db
