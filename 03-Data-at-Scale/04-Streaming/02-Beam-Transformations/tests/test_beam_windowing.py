import pytest
from tests.utils import (load_intermediate_output,
                         convert_string_eval,
                         sort_lower)

from datetime import datetime


@pytest.mark.optional
def test_read_type():
    """optional test, not checked by `make test`"""
    l_test = load_intermediate_output("./data","first_read")
    first_line = convert_string_eval(l_test[0])
    if first_line is None:
        first_line = l_test[0]
    assert type(first_line) == list
