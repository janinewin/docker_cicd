import pytest
import psycopg2
import os
import pathlib

challenge_path = pathlib.Path(__file__).parent.parent.absolute()

DATABASE_CONFIG = {
    "dbname": "pagila",
    "user": os.environ["POSTGRES_USER"],
    "password": os.environ["POSTGRES_PASSWORD"],
    "host": "0.0.0.0",
    "port": "5410",
}


@pytest.fixture
def db_connection():
    conn = psycopg2.connect(**DATABASE_CONFIG)
    yield conn
    conn.close()


def read_sql(filename):
    with open(filename, "r") as file:
        return file.read()


def test_search_query(db_connection):
    sql = read_sql(challenge_path / "text_search_query.sql")
    cursor = db_connection.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    cursor.close()
    assert str(results[0]) == "('INTENTIONS EMPIRE', 0.075990885)"


def test_recommendation_query(db_connection):
    sql = read_sql(challenge_path / "recommendation_query.sql")
    cursor = db_connection.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    cursor.close()
    assert str(results[0]) == "('ACADEMY DINOSAUR',)"


def test_improved_text_search_query(db_connection):
    sql = read_sql(challenge_path / "improved_text_search_query.sql")
    cursor = db_connection.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    cursor.close()
    assert str(results[0]) == "('BARBARELLA STREETCAR', 0.02)"
