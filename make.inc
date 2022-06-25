# Include this Makefile snippet with `include <relative path to>/make.inc`
# -- should be included in all exercises' Makefile

.PHONY: all
all: format test

.PHONY: pytest
pytest:
	@# The second time is to save its non-colored output to a file
	@PYTHONDONTWRITEBYTECODE=1 poetry run pytest -v 2>&1 > test_output.txt || echo "-- Some tests didn't pass, let's look at the output"
	@# Not ideal but works, we run `pytest -v` twice - the first time is with the nice colored output
	PYTHONDONTWRITEBYTECODE=1 poetry run pytest -v --color=yes

.PHONY: install
install:
	poetry install

.PHONY: format
format:
	poetry run black .
