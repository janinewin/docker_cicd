import os

import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.sensors.external_task import ExternalTaskSensor


AIRFLOW_HOME = os.getenv('AIRFLOW_HOME')


def read_parquet_file(input_file: str) -> pd.DataFrame:
    return pd.read_parquet(input_file)


def get_trips_longer_than(df, distance: int) -> pd.DataFrame:
    return df[df['trip_distance'] > distance]


def get_trips_more_expensive_than(df, amount: int) -> pd.DataFrame:
    return df[df['total_amount'] > amount]


def save_dataframe_to_parquet(df, output_file: str) -> None:
    df.to_parquet(output_file)


def filter_long_trips(input_file: str, output_file: str, distance: int) -> None:
    df = read_parquet_file(input_file)
    df = get_trips_longer_than(df, distance)
    save_dataframe_to_parquet(df, output_file)


def filter_expensive_trips(input_file: str, output_file: str, amount: int) -> None:
    df = read_parquet_file(input_file)
    df = get_trips_more_expensive_than(df, amount)
    save_dataframe_to_parquet(df, output_file)


def is_month_odd(ds_nodash: str) -> bool:
    return "filter_expensive_trips" if int(ds_nodash[6:8]) % 2 == 0 else "filter_long_trips"


with DAG(
        'transform',
        default_args={
            'depends_on_past': True,
            'start_date': '2021-06-01',
            'end_date': '2021-12-31'
        },
        schedule_interval='@monthly',
) as dag:

    data_url = 'https://nyc-tlc.s3.amazonaws.com/trip+data/yellow_tripdata_{{ ds_nodash }}.parquet'
    raw_data_file = f"{AIRFLOW_HOME}/data/bronze/yellow_tripdata_" + "{{ execution_date.strftime(\'%Y-%m\') }}.parquet"
    filtered_data_file = f"{AIRFLOW_HOME}/data/silver/yellow_tripdata_" + "{{ execution_date.strftime(\'%Y-%m\') }}.parquet"

    wait_for_extract = ExternalTaskSensor(
        task_id="extract_sensor",
        dag=dag,
        external_dag_id='extract',
        allowed_states=["success"],
        poke_interval=10,
        timeout=60*10,
    )

    check_if_month_is_odd_task = BranchPythonOperator(
        task_id="check_if_month_is_odd",
        dag=dag,
        python_callable=is_month_odd,
        op_kwargs={
            "date": "{{ ds_nodash }}",
        },
    )

    filter_long_trips_task = PythonOperator(
        task_id="filter_long_trips",
        python_callable=filter_long_trips,
        op_kwargs=dict(input_file=raw_data_file,
                       output_file=filtered_data_file, distance=100),
    )

    filter_expensive_trips_task = PythonOperator(
        task_id="filter_expensive_trips",
        python_callable=filter_expensive_trips,
        op_kwargs=dict(input_file=raw_data_file,
                       output_file=filtered_data_file, amount=500),
    )

    wait_for_extract >> check_if_month_is_odd_task >> [filter_expensive_trips_task, filter_long_trips_task]
