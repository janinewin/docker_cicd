include ../../../make.inc

test: pytest-and-write-output

run-server:
	poetry run uvicorn lwasync.server:app --port 8080

run-client-sync:
	poetry run python lwasync/client_synchronous.py --number 10

run-client-async:
	poetry run python lwasync/client_asynchronous.py --number 10
