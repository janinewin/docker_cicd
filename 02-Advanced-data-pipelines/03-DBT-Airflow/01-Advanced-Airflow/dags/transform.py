import os

import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.external_task import ExternalTaskSensor


AIRFLOW_HOME = os.getenv('AIRFLOW_HOME')


def read_parquet_file(input_file: str):
    return pd.read_parquet(input_file)


def get_trips_longer_than(df, distance: int):
    return df[df['trip_distance'] > distance]


def save_dataframe_to_parquet(df, output_file: str) -> None:
    df.to_parquet(output_file)


def filter_long_trips(input_file: str, output_file: str):
    df = read_parquet_file(input_file)
    df = get_trips_longer_than(df, 100)
    save_dataframe_to_parquet(df, output_file)


default_args = {
    'depends_on_past': True,
    'start_date': '2021-01-01',
    'end_date': '2021-12-31'
}

with DAG(
        'transform',
        default_args=default_args,
        description='A simple DAG to create a local etl',
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

    filter_long_trips_task = PythonOperator(
        task_id="filter_long_trips",
        python_callable=filter_long_trips,
        op_kwargs=dict(input_file=raw_data_file,
                       output_file=filtered_data_file),
    )

    wait_for_extract >> filter_long_trips_task
