import os
from datetime import datetime

# $IMPORT_BEGIN
# noreorder
import pandas as pd
from airflow.decorators import dag, task
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.operators.empty import EmptyOperator
from airflow.utils.dates import days_ago

AIRFLOW_HOME = os.getenv("AIRFLOW_HOME")

@dag(
    "transform",
    default_args={"depends_on_past": True},
    start_date=datetime(2021, 6, 1),
    end_date=datetime(2021, 12, 31),
    schedule_interval="@monthly",
)

def prepare_data(bronze_file: str, date: str):
        """
        - Converts data from `bronze_file` to DataFrame  using pandas
        - Adds a new column named 'date' that stores the current month (should be formatted as YYYY-MM)
        - Keeps only the ["date", "trip_distance" and "total_amount"] columns, in that order
        - Returns the DataFrame
        """
        pass  # YOUR CODE HERE

#New one
def transform():
    @task()
    def is_month_odd(date: str) -> str:
        """
        date: formatted as YYYY-MM.
        Returns "filter_expensive_trips" if the month date is even, "filter_long_trips" otherwise.
        """
        return "filter_expensive_trips" if int(date[-2:]) % 2 == 0 else "filter_long_trips"

    @task()
    def filter_long_trips(bronze_file: str, silver_file: str, date: str, distance: int) -> None:
        """
        - Calls prepare_data to get a cleaned DataFrame
        - Keep only rows for which the trip_distance's value is greater than `distance`
        - Saves the DataFrame to `silver_file` without keeping the DataFrame indexes
        """
        pass  # YOUR CODE HERE

    @task()
    def filter_expensive_trips(bronze_file: str, silver_file: str, date: str, amount: int) -> None:
        """
        - Calls prepare_data to get a cleaned DataFrame
        - Keep only rows for which the total_amount's value is greater than `amount`
        - Saves the DataFrame to `silver_file` without keeping the DataFrame indexes
        """
        pass  # YOUR CODE HERE

    # Organise your tasks hierachy here
    pass  # YOUR CODE HERE

transform()
