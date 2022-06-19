include ../../../make.inc

.PHONY: install test testTask1 testTask2 testTask3

testTask1:
	docker compose -f docker-compose-1.yml config
	poetry run  pytest -k TestTask1

testTask2:
	docker compose -f docker-compose-2.yml config
	poetry run pytest -k TestTask2

testTask3:
	docker compose -f docker-compose-3.yml config
	poetry run pytest -k TestTask3
