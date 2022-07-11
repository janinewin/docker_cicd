import os
from datetime import datetime

import pandas as pd
from airflow import DAG

# IMPORT YOUR PACKAGES HERE

AIRFLOW_HOME = os.getenv("AIRFLOW_HOME")


def is_month_odd(date: str) -> str:
    """
    Returns "filter_expensive_trips" if the month date is odd, "filter_long_trips" otherwise.
    Date should be formatted as YYYY-MM.
    """
    pass  # YOUR CODE HERE


def prepare_data(bronze_file: str, date: str):
    """
    - Converts data from `bronze_file` to DataFrame  using pandas
    - Adds a new column named 'date' that stores the current month (should be formatted as YYYY-MM)
    - Keeps only the date, trip_distance and total_amount columns (in that order)
    - Returns the DataFrame
    """
    pass  # YOUR CODE HERE


def filter_long_trips(bronze_file: str, silver_file: str, date: str, distance: int) -> None:
    """
    - Calls prepare_data to get a cleaned DataFrame
    - Keep only rows for which the trip_distance's value is greater than `distance`
    - Saves the DataFrame to `silver_file` without keeping the DataFrame indexes
    """
    pass  # YOUR CODE HERE


def filter_expensive_trips(bronze_file: str, silver_file: str, date: str, amount: int) -> None:
    """
    - Calls prepare_data to get a cleaned DataFrame
    - Keep only rows for which the total_amount's value is greater than `amount`
    - Saves the DataFrame to `silver_file` without keeping the DataFrame indexes
    """
    pass  # YOUR CODE HERE


with DAG(
    "transform",
    default_args={"depends_on_past": True},
    start_date=datetime(2021, 6, 1),
    end_date=datetime(2021, 12, 31),
    schedule_interval="@monthly",
) as dag:
    pass  # YOUR CODE HERE
