import os

import pendulum
from airflow import DAG
from airflow.operators.bash import BashOperator


DBT_DIR = os.getenv('DBT_DIR')


with DAG(
    "dbt",
    default_args={'depends_on_past': True, 'start_date': pendulum.today('UTC').add(days=-1)},
    schedule_interval='@daily',
    catchup=False
) as dag:

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"dbt run --profiles-dir {DBT_DIR} --project-dir {DBT_DIR}",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"dbt test --profiles-dir {DBT_DIR} --project-dir {DBT_DIR}",
    )

    dbt_run >> dbt_test
