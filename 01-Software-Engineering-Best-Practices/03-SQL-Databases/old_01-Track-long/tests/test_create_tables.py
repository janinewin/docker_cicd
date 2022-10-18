import os
import pathlib

import lewagonde


def test_correct_tables():
    lewagonde.load_dot_env(lewagonde.dot_env_path_sql())
    # print("OS ENVIRON : ", dict(os.environ))
    df_schemas = lewagonde.read_sql_query(
        "SELECT * \
        FROM INFORMATION_SCHEMA.TABLES \
        WHERE table_schema = 'public'",
        password=os.environ.get("POSTGRES_PASSWORD", ""),
        user="lewagon",
        host="localhost",
        dbname="db",
    )
    loaded_tables = set(df_schemas["table_name"].tolist())
    assert set(["movies_metadata", "ratings"]) <= loaded_tables, "Not all tables loaded, or incorrect table names"
