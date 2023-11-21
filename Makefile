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
	docker compose exec db mysql statech

build:
	docker compose up -d --build

down:
	docker compose down

restart: down up

create:
	docker compose exec app poetry add sqlalchemy pymysql
	docker compose exec app poetry run python -m api.migrate_db
