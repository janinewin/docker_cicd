import os

import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.sensors.external_task import ExternalTaskSensor
from sqlalchemy import create_engine

AIRFLOW_HOME = os.getenv('AIRFLOW_HOME')


def load_to_database(input_file: str, hook: PostgresHook):
    uri = hook.get_uri()
    df = pd.read_parquet(input_file)
    df.to_sql(name='trips', con=create_engine(uri), index=False, if_exists='append')


def is_month_odd(ds_nodash: str) -> bool:
    return "load_to_database" if int(ds_nodash[4:6]) % 2 == 0 else "load_to_database"


default_args = {
    'depends_on_past': True,
    'start_date': '2021-01-01',
    'end_date': '2021-12-31'
}

with DAG(
        'load',
        default_args=default_args,
        description='A simple DAG to create a local etl',
        schedule_interval='@monthly',
) as dag:

    filtered_data_file = f"{AIRFLOW_HOME}/data/silver/yellow_tripdata_" + "{{ execution_date.strftime(\'%Y-%m\') }}.parquet"

    wait_for_transform = ExternalTaskSensor(
        task_id="transform_sensor",
        dag=dag,
        external_dag_id='transform',
        allowed_states=["success"],
        poke_interval=10,
        timeout=60*10,
    )

    check_if_month_is_odd_task = BranchPythonOperator(
        task_id="check_if_mont_is_odd",
        dag=dag,
        python_callable=is_month_odd,
        op_kwargs={
            "date": "{{ ds_nodash }}",
        },
    )

    hook = PostgresHook(postgres_conn_id='postgres_connection')

    load_to_database_task = PythonOperator(
        task_id="load_to_database",
        python_callable=load_to_database,
        op_kwargs=dict(input_file=filtered_data_file, hook=hook)
    )

    wait_for_transform >> check_if_month_is_odd_task >> [load_to_database_task, load_to_database_task]
