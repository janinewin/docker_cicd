include ../../../make.inc

.PHONY: install test testTask1 testTask2 testTask3

testTask1:
	docker compose -f docker-compose-1.yml config
	PYTHONDONTWRITEBYTECODE=1 poetry run pytest -v --color=yes -k TestTask1

testTask2:
	docker compose -f docker-compose-2.yml config
	PYTHONDONTWRITEBYTECODE=1 poetry run pytest -v --color=yes -k TestTask2

testTask3:
	docker compose -f docker-compose-3.yml config
	PYTHONDONTWRITEBYTECODE=1 poetry run pytest -v --color=yes -k TestTask3
