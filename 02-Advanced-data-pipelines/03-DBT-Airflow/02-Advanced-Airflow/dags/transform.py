import os

import pandas as pd
from airflow import DAG

# IMPORT YOUR PACKAGES HERE

AIRFLOW_HOME = os.getenv("AIRFLOW_HOME")


def is_month_odd(ds_nodash: str) -> str:
    """
    Returns filter_expensive_trips if the month date is odd, filter_long_trips otherwise.
    Date should be formatted as YYYY-MM-DD.
    """
    pass  # YOUR CODE HERE


def read_parquet_file(input_file: str) -> pd.DataFrame:
    """
    Reads the parquet file using pandas and returns the corresponding DataFrame.
    """
    pass  # YOUR CODE HERE


def get_trips_longer_than(df, distance: int) -> pd.DataFrame:
    """
    Returns a filtered version of df with rows for which the 'trip_distance'
    is greater than the `distance`.
    """
    pass  # YOUR CODE HERE


def get_trips_more_expensive_than(df, amount: int) -> pd.DataFrame:
    """
    Returns a filtered version of df with rows for which the 'total_amount'
    is greater than the `amount`.
    """
    pass  # YOUR CODE HERE


def save_dataframe_to_parquet(df, output_file: str) -> None:
    """
    Saves df to a parquet file named `output_file`.
    """
    pass  # YOUR CODE HERE


def filter_long_trips(input_file: str, output_file: str, distance: int) -> None:
    """
    Reuses read_parquet_file, get_trips_longer_than and save_dataframe_to_parquet
    functions to get the data from bronze, filter it and save it to silver.
    """
    pass  # YOUR CODE HERE


def filter_expensive_trips(input_file: str, output_file: str, amount: int) -> None:
    """
    Reuses read_parquet_file, get_trips_more_expensive_than and save_dataframe_to_parquet
    functions to get the data from bronze, filter it and save it to silver.
    """
    pass  # YOUR CODE HERE


with DAG(
    "transform",
    # YOUR CODE HERE
) as dag:
    pass  # YOUR CODE HERE
