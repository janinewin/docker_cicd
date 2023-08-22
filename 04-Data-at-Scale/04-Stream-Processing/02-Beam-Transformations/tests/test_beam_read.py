import pytest
from tests.utils import load_intermediate_output, convert_string_eval


@pytest.mark.optional
def test_read_type():
    """Check that each line created is of the "form":
    ['AtmP', '996.0840610169381', '2022-11-25 09:00:00.334685']
    """

    output_lines_to_test = load_intermediate_output("./data", "first_read")
    first_line = convert_string_eval(output_lines_to_test[0])
    if first_line is None:
        first_line = output_lines_to_test[0]

    assert type(first_line) == list
    assert len(first_line) == 3
