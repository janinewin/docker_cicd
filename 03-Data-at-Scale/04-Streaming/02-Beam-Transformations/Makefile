include ../../../make.inc

.PHONY: test_first_read
test_first_read:
	@pytest tests/test_beam_read.py --disable-pytest-warnings -v

.PHONY: test_windowing
test_windowing:
	@pytest tests/test_beam_windowing.py --disable-pytest-warnings -v

.PHONY: test_beam_output
test_beam_output:
	@pytest tests/test_beam_output.py --disable-pytest-warnings -v

.PHONY: test
test: pytest-and-write-output
