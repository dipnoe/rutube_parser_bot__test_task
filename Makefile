docker-up:
	docker compose --env-file=.env up --build -d
lint:
	pylint src/ --ignore=alembic