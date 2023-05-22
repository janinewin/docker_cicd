from lewagonde import (
    __version__,
    soft_equal,
    docker_compose_equal_content,
    docker_compose_transform_dict_block,
)

import yaml


def test_version():
    assert __version__ == "0.1.0"


def test_transform_sql():
    sql_1 = """
    -- this is a comment
    SELECT * FROM
    table_1;
    """
    sql_2 = """
    SELECT * FROM table_1  ;
    """
    assert soft_equal(sql_1, sql_2, comment_chars="--")

    sql_3 = """
    SELECT * FROM table_1 JOIN table_2;
    """
    assert not soft_equal(sql_1, sql_3, comment_chars="--")

    py_1 = """# hello
    def print():
        ok
    # world
    """
    py_2 = """
    def print():
        ok
    """
    assert soft_equal(py_1, py_2, comment_chars="#")


def test_docker_compose_equal():
    dc1 = yaml.safe_load(
        """
version: '3.9'
services:
  webapi:
    container_name: fastapi
    build:
      context: .
      dockerfile: dockerfile-fastapi
  ok:
    environment:
      A: 10
      Bcd: 100
    """
    )

    dc2 = yaml.safe_load(
        """
services:
  ok:
    environment:
      - A=10
      - Bcd='100'
  webapi:
    build:
      dockerfile: dockerfile-fastapi
      context: .
    container_name: fastapi
version: '3.9'
    """
    )

    assert docker_compose_equal_content(dc1, dc2)

    dc1_str = "services:ok:environment:A:10Bcd:100webapi:build:context:.dockerfile:dockerfile-fastapicontainer_name:fastapiversion:3.9"
    assert docker_compose_transform_dict_block(dc1) == dc1_str
