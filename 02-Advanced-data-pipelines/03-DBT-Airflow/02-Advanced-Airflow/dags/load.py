import logging
import os
from datetime import datetime
from sqlite3 import Connection
from typing import Union

from airflow import DAG
from airflow.hooks.sqlite_hook import SqliteHook
from airflow.models.taskinstance import TaskInstance
from airflow.providers.postgres.hooks.postgres import PostgresHook
from sqlalchemy.engine.base import Engine

# IMPORT YOUR PACKAGES HERE

AIRFLOW_HOME = os.getenv("AIRFLOW_HOME")


def create_connection_from_hook(hook: Union[SqliteHook, PostgresHook]) -> Union[Engine, Connection]:
    """
    Creates a database connection from a PostgresHook/SqliteHook.
    """
    if hook.__class__.__name__ == "PostgresHook":
        return hook.get_sqlalchemy_engine()
    return hook.get_conn()


def load_to_database(input_file: str, date: str, hook: PostgresHook, task_instance: TaskInstance):
    """
    - Removes data from current date if exist by using the PostgresHook
    - Uses pandas functions to create a DataFrame from a csv file
    - Calls create_connection_from_hook to get a database connection from the hook
    - Calls to_sql function from pandas to insert data to the database (by passing the created_connection)
    - Uses xcom_push to export the number of inserted values (under the key `number_of_inserted_rows`)
    """
    pass  # YOUR CODE HERE


def display_number_of_inserted_rows(task_instance: TaskInstance):
    """
    Uses xcom_pull to get the number of inserted values to database and log it.
    The log should be formatted as "number_of_inserted_rows trips have been inserted".
    """
    pass  # YOUR CODE HERE


with DAG(
    "load",
    default_args={"depends_on_past": True},
    start_date=datetime(2021, 6, 1),
    end_date=datetime(2021, 12, 31),
    schedule_interval="@monthly",
) as dag:
    pass  # YOUR CODE HERE
