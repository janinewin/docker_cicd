include ../../../make.inc

.PHONY: test
test: pytest-and-write-output

.PHONY: test_first_read
test_first_read:
	@pytest tests/test_beam_read.py --disable-pytest-warnings


.PHONY: test_windowing
test_windowing:
	@pytest tests/test_beam_windowing.py --disable-pytest-warnings

.PHONY: test_grouping_by_key
test_grouping_by_key:
	@pytest tests/test_beam_grouping.py --disable-pytest-warnings
