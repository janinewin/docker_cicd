import logging
import os

import pandas as pd
from airflow import DAG
from airflow.models.taskinstance import TaskInstance
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.sensors.external_task import ExternalTaskSensor

AIRFLOW_HOME = os.getenv('AIRFLOW_HOME')


def create_connection_from_hook(hook):
    if hook.__class__.__name__ == 'PostgresHook':
        return hook.get_sqlalchemy_engine()
    return hook.get_conn()


def load_to_database(input_file: str, hook: PostgresHook, task_instance: TaskInstance):
    df = pd.read_parquet(input_file)
    task_instance.xcom_push('number_of_inserted_rows', len(df.index))
    df.to_sql(name='trips', con=create_connection_from_hook(hook), index=False, if_exists='append')


def display_number_of_inserted_rows(task_instance):
    number_of_inserted_rows = task_instance.xcom_pull(task_ids=['load_to_database'], key='number_of_inserted_rows')
    logging.info(f"{number_of_inserted_rows[0]} trips have been inserted")


default_args = {
    'depends_on_past': True,
    'start_date': '2021-06-01',
    'end_date': '2021-12-31'
}

with DAG(
        'load',
        default_args=default_args,
        schedule_interval='@monthly',
) as dag:

    filtered_data_file = f"{AIRFLOW_HOME}/data/silver/yellow_tripdata_" + "{{ execution_date.strftime(\'%Y-%m\') }}.parquet"

    wait_for_transform_task = ExternalTaskSensor(
        task_id="transform_sensor",
        dag=dag,
        external_dag_id='transform',
        allowed_states=["success"],
        poke_interval=10,
        timeout=60*10,
    )

    hook = PostgresHook(postgres_conn_id='postgres_connection')

    load_to_database_task = PythonOperator(
        task_id="load_to_database",
        python_callable=load_to_database,
        op_kwargs=dict(input_file=filtered_data_file, hook=hook)
    )

    display_number_of_inserted_rows_task = PythonOperator(
        task_id="display_number_of_inserted_rows",
        python_callable=display_number_of_inserted_rows
    )

    wait_for_transform_task >> load_to_database_task >> display_number_of_inserted_rows_task
