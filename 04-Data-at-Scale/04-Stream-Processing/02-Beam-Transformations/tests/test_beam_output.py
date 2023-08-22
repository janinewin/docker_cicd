from tests.utils import load_intermediate_output, convert_string_eval, sort_lower

from datetime import datetime


def test_final_output_type():
    """mandatory test
    test if final output is rows of dictionnaries
    """
    l_test = load_intermediate_output("./data", "output.txt")
    first_line = convert_string_eval(l_test[0])
    assert type(first_line) == dict


def test_final_output_schema():
    """mandatory test
    test the key expected inside of the dictionnaries
    """
    l_test = load_intermediate_output("./data", "output.txt")
    key_output = convert_string_eval(l_test[0])
    key_expected = ["Timestamp", "AtmP", "Temp", "Airtight", "H2OC"]

    assert sort_lower(key_expected) == sort_lower(key_output)


def test_final_output_fix_interval():
    """mandatory test
    test the each element is grouped by a fix interval
    """
    l_test = load_intermediate_output("./data", "output.txt")
    first_lines = [convert_string_eval(l_test[i]) for i in range(3)]
    key_timestamp = ""
    for key in first_lines[0].keys():
        if "timestamp" in key.lower():
            key_timestamp = key
    fmt_time = "%Y-%m-%d %H:%M:%S.%f"
    timestamps = [datetime.strptime(el[key_timestamp], fmt_time) for el in first_lines]
    interval_1, interval_2 = (
        timestamps[2] - timestamps[1],
        timestamps[1] - timestamps[0],
    )
    assert interval_1 == interval_2
