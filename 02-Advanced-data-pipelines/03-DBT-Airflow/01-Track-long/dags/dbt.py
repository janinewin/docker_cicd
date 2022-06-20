import json
import os

import pendulum
from airflow import DAG
from airflow.operators.bash import BashOperator


DBT_DIR = os.getenv('DBT_DIR')

DBT_ENV = {
    "DBT_USER": "{{ conn.postgres.login }}",
    "DBT_ENV_SECRET_PASSWORD": "{{ conn.postgres.password }}",
    "DBT_HOST": "{{ conn.postgres.host }}",
    "DBT_SCHEMA": "{{ conn.postgres.schema }}",
    "DBT_PORT": "{{ conn.postgres.port }}",
}


def load_manifest(file: str):
    with open(file) as f:
        data = json.load(f)
    return data


def make_dbt_task(node, dbt_verb):
    """Returns an Airflow operator either run and test an individual model"""
    GLOBAL_CLI_FLAGS = "--no-write-json"
    if dbt_verb == "run":
        model = node.split(".")[-1]
        task_id = node
    elif dbt_verb == "test":
        model = node.split(".")[-2]
        task_id = ".".join(node.split(".")[:-1])

    return BashOperator(
        task_id=task_id,
        bash_command=(
            f"dbt {GLOBAL_CLI_FLAGS} {dbt_verb} --target dev --models {model} "
            f"--profiles-dir {DBT_DIR} --project-dir {DBT_DIR}"
        ),
        env=DBT_ENV,
    )


def create_tasks(data: dict) -> dict:
    dbt_tasks = {}
    for node in data["nodes"].keys():
        if node.split(".")[0] == "model":
            dbt_tasks[node] = make_dbt_task(node, "run")
        elif node.split(".")[0] == "test":
            dbt_tasks[node] = make_dbt_task(node, "test")
    return dbt_tasks


def create_dags_dependencies(data: dict, dbt_tasks: dict):
    for node in data["nodes"].keys():
        if node.split(".")[0] in ("model", "test"):
            for upstream_node in data["nodes"][node]["depends_on"]["nodes"]:
                upstream_node_type = upstream_node.split(".")[0]
                if upstream_node_type in ("model", "test"):
                    dbt_tasks[upstream_node] >> dbt_tasks[node]


with DAG(
    "dbt",
    default_args={'depends_on_past': False, 'start_date': pendulum.today('UTC').add(days=-1)},
    schedule_interval='@daily',
    catchup=True
) as dag:

    data = load_manifest(f"{DBT_DIR}/target/manifest.json")
    dbt_tasks = create_tasks(data)
    create_dags_dependencies(data, dbt_tasks)
