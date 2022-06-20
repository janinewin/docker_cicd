# Include this Makefile snippet with `include <relative path to>/make.inc`
# -- should be included in all exercises' Makefile

.PHONE: all
all: format test

.PHONY: test
test:
	poetry run pytest -v

.PHONY: install
install:
	poetry install

.PHONY: format
format:
	poetry run black .
