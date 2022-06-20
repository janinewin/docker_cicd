import os

from airflow import DAG

# IMPORT YOUR PACKAGES HERE


AIRFLOW_HOME = os.getenv("AIRFLOW_HOME")


with DAG(
    "extract",
    # YOUR CODE HERE
) as dag:
    pass  # YOUR CODE HERE
