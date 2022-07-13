import json
import os
import pandas as pd
import pathlib
import time
from typing import Tuple

import lewagonde


def json_to_df(json_fp: str) -> pd.DataFrame:
    """
    Take the IKEA raw JSON data file path as input, load it, and return a pandas dataframe.
    """
    pass  # YOUR CODE HERE


def save_df_to_parquet(df: pd.DataFrame, pq_fp: str):
    """
    Store the DataFrame to a Parquet file
    """
    pass  # YOUR CODE HERE


def cast_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Takes the raw DataFrame as input and returns a new DataFrame with columns having appropriate types.
    """
    pass  # YOUR CODE HERE


def save_df_to_csv(df: pd.DataFrame, csv_fp: str):
    """
    Store the DataFrame to a CSV
    """
    pass  # YOUR CODE HERE


def query_perf(sql_query: str = "", sql_file_path: str = "") -> Tuple[float, pd.DataFrame]:
    """
    Measure a query performance by passing EITHER a `sql_query` string of the `sql_file_path`.
    """
    assert len([q for q in [sql_query,  sql_file_path] if q != ""]) == 1
    if sql_file_path != "":
        sql_query = open(sql_file_path).read()
    parent_dir = pathlib.Path(os.path.realpath(__file__)).parent.parent
    dot_env_fp = os.path.join(parent_dir, ".env")
    lewagonde.load_dot_env(dot_env_fp)

    con = lewagonde.get_db_connection(
        password=os.environ["POSTGRES_PASSWORD"], user="lewagon", host="0.0.0.0", dbname="db",
    )

    try:
        t0 = time.time()
        result_df = pd.read_sql_query(
            sql=sql_query,
            con=con,
        )
        dt_seconds = time.time() - t0
        return dt_seconds, result_df
    except BaseException as e:
        raise e
    finally:
        con.close()
