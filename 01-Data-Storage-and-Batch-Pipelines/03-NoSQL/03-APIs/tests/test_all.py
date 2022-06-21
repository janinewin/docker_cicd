import os


def test_time_format():
    from lwapi import jsonrpc
    hms = jsonrpc.time()
    assert isinstance(hms["h"], int)
    assert isinstance(hms["m"], int)
    assert isinstance(hms["s"], int)


def test_there_is_a_csv_file():
    from lwapi import rural
    assert os.path.isfile(rural.get_rural_csv_fp()), "file API-rural.csv not found under data/"


def test_rural_population_percentage_json():
    from lwapi import jsonrpc
    assert jsonrpc.rural_population_percentage("France", 1964) == 34.102
