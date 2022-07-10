import argparse
import time
from unittest import mock


def test_sync_one():
    from lwasync import client_synchronous
    response = client_synchronous.make_one_call()
    assert isinstance(response, dict)


def test_sync_many():
    from lwasync import client_synchronous
    responses = client_synchronous.make_many_calls(2)
    assert isinstance(responses, list)


@mock.patch("argparse.ArgumentParser.parse_args", return_value=argparse.Namespace(number=4))
def test_faster(mock_args):
    from lwasync import client_synchronous, client_asynchronous
    tsync0 = time.time()
    client_synchronous.main()
    tsync = time.time() - tsync0

    tasync0 = time.time()
    client_asynchronous.main()
    tasync = time.time() - tasync0

    assert tsync > tasync
