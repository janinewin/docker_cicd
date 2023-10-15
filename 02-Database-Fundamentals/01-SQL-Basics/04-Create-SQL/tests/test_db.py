import pytest
import os
from lwsql.db import DB


@pytest.fixture
def temp_db_file():
    db_filename = "test_database.db"
    with DB(db_filename) as db:
        yield db
    os.remove(db_filename)


def test_create_table(temp_db_file):
    create_table_sql = "CREATE TABLE students (id int, name str, age int)"
    temp_db_file.execute_sql(create_table_sql)
    metadata = temp_db_file.btree.read_metadata()
    assert "students" in metadata["tables"]


def test_insert_data(temp_db_file):
    create_table_sql = "CREATE TABLE students (id int, name str, age int)"
    temp_db_file.execute_sql(create_table_sql)
    insert_sql = "INSERT INTO students VALUES (1, 'Alice', 30)"
    temp_db_file.execute_sql(insert_sql)
    row = temp_db_file.btree.search(1)
    assert row is not None
    assert row["id"] == 1
    assert row["name"] == "Alice"
    assert row["age"] == 30


def test_select_data(temp_db_file):
    create_table_sql = "CREATE TABLE students (id int, name str, age int)"
    temp_db_file.execute_sql(create_table_sql)
    insert_sql = "INSERT INTO students VALUES (1, 'Alice', 30)"
    temp_db_file.execute_sql(insert_sql)
    select_sql = "SELECT name, age FROM students"
    result = temp_db_file.execute_sql(select_sql)
    assert len(result) == 1
    assert "id" not in result[0]
    assert result[0]["name"] == "Alice"
    assert result[0]["age"] == 30


def test_invalid_sql(temp_db_file):
    invalid_sql = "INVALID SQL STATEMENT"
    with pytest.raises(Exception):
        temp_db_file.execute_sql(invalid_sql)


if __name__ == "__main__":
    pytest.main()
