import pytest
from tests.utils import load_intermediate_output, convert_string_eval

from datetime import datetime


@pytest.mark.optional
def test_read_type():
    """
    Check that each line generated is in the "form":
    ('2022-11-25 09:00:15.000000', ['AtmP', 996.0840610169381])
    """
    output_lines_to_test = load_intermediate_output("./data", "windowing")
    first_line = convert_string_eval(output_lines_to_test[0])
    if first_line is None:
        first_line = output_lines_to_test[0]

    assert type(first_line) == tuple
    assert len(first_line) == 2
    assert datetime.strptime(first_line[0], "%Y-%m-%d %H:%M:%S.%f")
    assert type(first_line[1]) == list
    assert len(first_line[1]) == 2
