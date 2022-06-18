import os

import pandas as pd
import psycopg2 as pg
from psycopg2 import extensions as pgext

from lewagonde import constants


def get_db_connection(
    password: str = os.environ.get(constants.ENV_DB_READONLY_PASSWORD, ""),
    user: str = os.environ.get(constants.ENV_DB_READONLY_USER, ""),
    host: str = os.environ.get(constants.ENV_DB_HOST, ""),
    dbname: str = os.environ.get(constants.ENV_DB_NAME, ""),
) -> pgext.connection:
    """
    _get_db_connection will get you a Postgres connection
    Try not to use directly, prefer the pd_read_sql_query helper which will open and close the DB connection for you

    Helper method to get a Postgres DB connection, with sane read-only overridable defaults
    """
    return pg.connect(f"host={host} dbname={dbname} user={user} password={password}")


def read_sql_query(
    sql: str,
    index_col=None,
    coerce_float=True,
    params=None,
    parse_dates=None,
    chunksize=None,
    dtype=None,
    password: str = os.environ.get(constants.ENV_DB_READONLY_PASSWORD, ""),
    user: str = os.environ.get(constants.ENV_DB_READONLY_USER, ""),
    host: str = os.environ.get(constants.ENV_DB_HOST, ""),
    dbname: str = os.environ.get(constants.ENV_DB_NAME, ""),
) -> pd.DataFrame:
    """
    read_sql_query wraps pandas.read_sql_query,
    handles the PDB read only connection creation and closing once the query is executed
    """
    con = get_db_connection(password=password, user=user, host=host, dbname=dbname)
    try:
        return pd.read_sql_query(
            sql=sql,
            con=con,
            index_col=index_col,
            coerce_float=coerce_float,
            params=params,
            parse_dates=parse_dates,
            chunksize=chunksize,
            dtype=dtype,
        )
    except BaseException as e:
        raise e
    finally:
        con.close()

