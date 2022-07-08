import os

from airflow import DAG
from airflow.operators.bash import BashOperator

# IMPORT YOUR PACKAGES HERE

DBT_DIR = os.getenv("DBT_DIR")


def load_manifest(file: str) -> dict:
    """
    Reads the json `file` and returns it as a dict.
    """
    pass  # YOUR CODE HERE


def make_dbt_task(node: str, dbt_verb: str) -> BashOperator:
    """
    Returns a BashOperator with a bash command to run or test the given node.
    Adds the project-dir argument and names the tasks as shown by the below examples.
    Cleans the node's name when it is a test.

    Examples:
    >>> print(make_dbt_task('model.dbt_lewagon.my_first_dbt_model', 'run'))
    BashOperator(
        task_id=model.dbt_lewagon.my_first_dbt_model,
        bash_command= "dbt run --models my_first_dbt_model --project-dir /opt/airflow/lewagon_dbt"
    )

    >>> print(make_dbt_task('test.dbt_lewagon.not_null_my_first_dbt_model_id.5fb22c2710', 'test'))
    BashOperator(
        task_id=test.dbt_lewagon.not_null_my_first_dbt_model_id,
        bash_command= "dbt test --models not_null_my_first_dbt_model_id --project-dir /opt/airflow/lewagon_dbt"
    )
    """
    pass  # YOUR CODE HERE


def create_tasks(data: dict) -> dict:
    """
    This function should iterate through data["nodes"] keys and call make_dbt_task
    to build and return a new dict containing as keys all nodes' names and their corresponding dbt tasks as values.
    """
    pass  # YOUR CODE HERE


def create_dags_dependencies(data: dict, dbt_tasks: dict):
    """
    Iterate over every node and their dependencies (by using data and the "depends_on" key)
    to order the Airflow tasks properly.
    """
    pass  # YOUR CODE HERE


with DAG(
    "dbt_advanced",
    # YOUR CODE HERE
) as dag:

    data = load_manifest(f"{DBT_DIR}/manifest.json")
    dbt_tasks = create_tasks(data)
    create_dags_dependencies(data, dbt_tasks)
