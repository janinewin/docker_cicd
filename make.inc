# Include this Makefile snippet with `include <relative path to>/make.inc`
# -- should be included in all exercises' Makefile

.PHONY: all
all: format pytest-and-write-output

.PHONY: pytest-and-write-output
pytest-and-write-output:
	@# The first time we save its non-colored output to a file
	@PYTHONDONTWRITEBYTECODE=1 pytest tests -m "not optional" -v --disable-warnings 2>&1 > test_output.txt || echo "-- Some tests didn't pass, let's look at the output"
	@# The second time we print results with a nice colored output (Not ideal but works)
	PYTHONDONTWRITEBYTECODE=1 pytest tests -m "not optional" -v --disable-warnings --color=yes

.PHONY: install
install:
	poetry install

.PHONY: format
format:
	black .
