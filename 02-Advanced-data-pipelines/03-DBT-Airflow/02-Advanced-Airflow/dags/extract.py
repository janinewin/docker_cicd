import os
from datetime import datetime

from airflow import DAG

# IMPORT YOUR PACKAGES HERE


AIRFLOW_HOME = os.getenv("AIRFLOW_HOME")

with DAG(
    "extract",
    default_args={"depends_on_past": True},
    start_date=datetime(2021, 6, 1),
    end_date=datetime(2021, 12, 31),
    schedule_interval="@monthly",
) as dag:
    pass  # YOUR CODE HERE
