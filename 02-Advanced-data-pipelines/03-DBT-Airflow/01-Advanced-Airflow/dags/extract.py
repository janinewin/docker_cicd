import os

from airflow import DAG
from airflow.operators.bash import BashOperator


AIRFLOW_HOME = os.getenv('AIRFLOW_HOME')

default_args = {
    'depends_on_past': True,
    'start_date': '2021-01-01',
    'end_date': '2021-12-31'
}

with DAG(
        'extract',
        default_args=default_args,
        description='A simple DAG to get monthly data',
        schedule_interval='@monthly',
) as dag:

    url = "https://nyc-tlc.s3.amazonaws.com/trip+data/yellow_tripdata_{{ execution_date.strftime(\'%Y-%m\') }}.parquet"
    file_path = f"{AIRFLOW_HOME}/data/bronze/yellow_tripdata_" + "{{ execution_date.strftime(\'%Y-%m\') }}.parquet"

    get_parquet_file_task = BashOperator(
        task_id='get_parquet_file',
        bash_command=f"curl {url} > {file_path}"
    )

    get_parquet_file_task
