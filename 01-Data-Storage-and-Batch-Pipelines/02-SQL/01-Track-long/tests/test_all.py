import os
import pathlib

from lewagonde import read_sql_query, load_dot_env


def test_query():
    parent_dir = pathlib.Path(os.path.realpath(__file__)).parent.parent
    dot_env_fp = os.path.join(parent_dir, ".env")

    load_dot_env(dot_env_fp)

    dataframe = read_sql_query("SELECT * FROM ...",
            password = os.environ.get(constants.ENV_DB_READONLY_PASSWORD, ""),
            user = os.environ.get(constants.ENV_DB_READONLY_USER, ""),
            host = os.environ.get(constants.ENV_DB_HOST, ""),
            dbname = os.environ.get(constants.ENV_DB_NAME, "")
        )
