import os

from pytest import approx


def test_http_time_format():
    from src import json_rest
    hms = json_rest.time()
    assert isinstance(hms["h"], int)
    assert isinstance(hms["m"], int)
    assert isinstance(hms["s"], int)


def test_grpc_time_format():
    from src import proto_rpc_server
    api = proto_rpc_server.Api()
    response = api.get_time(proto_rpc_server.api_pb2.TimeRequest(), None)
    assert isinstance(response.h, int)
    assert isinstance(response.m, int)
    assert isinstance(response.s, int)


def test_there_is_a_csv_file():
    from src import rural
    assert os.path.isfile(rural.get_rural_csv_fp()), "file API-rural.csv not found under data/"


def test_rural_population_percentage_http():
    from src import json_rest
    assert json_rest.rural_population_percentage("France", 1964) == approx(34.102)


def test_rural_population_percentage_grpc():
    from src import proto_rpc_server
    api = proto_rpc_server.Api()
    response = api.get_rural_population_percentage(proto_rpc_server.api_pb2.RuralRequest(year=1964, country="France"), None)
    assert response.value == approx(34.102)
