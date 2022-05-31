import json
import os

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.dates import days_ago
from googletrans import Translator

AIRFLOW_HOME = os.getenv('AIRFLOW_HOME')


def read_from_json(joke_file: str) -> dict:
    """
    Reads and returns the content of the `joke_file`.
    """
    with open(joke_file, 'r') as file:
        return json.load(file)


def translate_joke_to_swedish(joke: str) -> str:
    """
    Returns the translated to Swedish joke using
    the googletrans library: https://github.com/ssut/py-googletrans
    """
    translator = Translator()
    return translator.translate(joke, dest='sv').text


def write_jokes_to_json(swedified_joke_file: str, joke: str, swedified_joke: str) -> None:
    """
    Creates a json file named `swedified_joke_file` with two keys 'joke'
    and 'swedified_joke' and their corresponding values.
    """
    with open(swedified_joke_file, 'w') as file:
        json.dump({'joke': joke, 'swedified_joke': swedified_joke}, file)


def double_single_quote(joke: str):
    """
    Returns the `joke` with all single quotes
    replaced by two single quotes (not a double quote).
    """
    return joke.replace("'", "''")


def transform(joke_file: str, swedified_joke_file: str) -> None:
    """
    Uses the read_from_json, translate_joke_to_swedish,
    double_single_quote and write_jokes_to_json functions to
    transform your data as expected.
    """
    joke = read_from_json(joke_file)["value"]
    swedified_joke = translate_joke_to_swedish(joke)
    write_jokes_to_json(swedified_joke_file, double_single_quote(joke), double_single_quote(swedified_joke))


def load(swedified_joke_file: str, hook: PostgresHook) -> None:
    """
    Uses read_from_json function to get the contents
    of `swedified_joke_file`. Then, loads it into
    the PostgreSQL database using the PostgresHook.
    """
    joke_values = read_from_json(swedified_joke_file)

    hook.run(sql=f"""
                INSERT INTO swedified_jokes (joke, swedified_joke)
                VALUES ('{joke_values['joke']}', '{joke_values['swedified_joke']}')""")


default_args = {
    'depends_on_past': True,
    'start_date': days_ago(5),
}

with DAG(
        'local_etl',
        default_args=default_args,
        description='A local etl',
        schedule_interval='@daily',
        catchup=True
) as dag:

    data_url = 'https://api.chucknorris.io/jokes/random'
    joke_file = f"{AIRFLOW_HOME}/data/bronze/joke_" + "{{ds_nodash}}.json"
    swedified_joke_file = f"{AIRFLOW_HOME}/data/silver/swedified_joke_" + "{{ds_nodash}}.json"

    create_swedified_jokes_task = PostgresOperator(
        task_id="create_swedified_jokes_table",
        sql="""CREATE TABLE IF NOT EXISTS swedified_jokes (
                id SERIAL PRIMARY KEY,
                joke VARCHAR NOT NULL,
                swedified_joke VARCHAR NOT NULL
            );""",
        postgres_conn_id='postgres_connection'
    )

    extract_task = BashOperator(
        task_id='extract',
        bash_command=f'curl {data_url} > {joke_file}')

    transform_task = PythonOperator(
        task_id="transform",
        python_callable=transform,
        op_kwargs=dict(joke_file=joke_file,
                       swedified_joke_file=swedified_joke_file),
    )

    hook = PostgresHook(postgres_conn_id='postgres_connection')

    load_task = PythonOperator(
        task_id="load",
        python_callable=load,
        op_kwargs=dict(swedified_joke_file=swedified_joke_file, hook=hook),
    )

    create_swedified_jokes_task >> extract_task >> transform_task >> load_task
