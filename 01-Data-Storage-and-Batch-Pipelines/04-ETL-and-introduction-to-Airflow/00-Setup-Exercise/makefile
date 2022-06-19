include ../../../make.inc

.PHONY: install test_docker_compose test_dockerfile test_files_and_folders test

test_docker_compose:
	poetry run pytest -v tests/test_docker_compose.py

test_dockerfile:
	poetry run pytest -v tests/test_dockerfile.py

test_files_and_folders:
	poetry run pytest -v tests/test_files_and_folders.py
