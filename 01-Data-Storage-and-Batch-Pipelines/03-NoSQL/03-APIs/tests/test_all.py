import os

from pytest import approx


def test_http_time_format():
    from lwapi import jsonrpc
    hms = jsonrpc.time()
    assert isinstance(hms["h"], int)
    assert isinstance(hms["m"], int)
    assert isinstance(hms["s"], int)


def test_grpc_time_format():
    from lwapi import protorpc
    api = protorpc.Api()
    response = api.GetTime(protorpc.api_pb2.TimeRequest(), None)
    assert isinstance(response.h, int)
    assert isinstance(response.m, int)
    assert isinstance(response.s, int)


def test_there_is_a_csv_file():
    from lwapi import rural
    assert os.path.isfile(rural.get_rural_csv_fp()), "file API-rural.csv not found under data/"


def test_rural_population_percentage_http():
    from lwapi import jsonrpc
    assert jsonrpc.rural_population_percentage("France", 1964) == approx(34.102)


def test_rural_population_percentage_grpc():
    from lwapi import protorpc
    api = protorpc.Api()
    response = api.GetRuralPopulationPercentage(protorpc.api_pb2.RuralRequest(year=1964, country="France"), None)
    assert response.value == approx(34.102)
