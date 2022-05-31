import os

import requests
from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.dates import days_ago


AIRFLOW_HOME = os.getenv('AIRFLOW_HOME')
COMMENTS_API_ROOT = "https://comments-api"


def get_last_comments() -> dict:
    """
    Calls COMMENTS_API_ROOT
    and returns the 'comments' field of the answer.
    """
    return requests.get(COMMENTS_API_ROOT).json()['comments']


def double_single_quote(comment: str):
    """
    Returns the `comment` with all single quotes
    replaced by two single quotes (not a double quote).
    """
    return comment.replace("'", "''")


def load_to_database(comments: list, hook) -> None:
    """
    Iterates over the comments, uses double_single_quote function
    to clean each comment and loads it into
    the PostgreSQL database using the PostgresHook.
    """
    for comment in comments:
        hook.run(sql=f"""
                    INSERT INTO comments (movie_id, comment, rating)
                    VALUES ({comment['movie_id']}, '{double_single_quote(comment['comment'])}', {comment['rating']})""")


def get_and_insert_last_comments(hook: PostgresHook) -> str:
    """
    Uses get_last_comments and load_to_database functiosn to get
    the last comments and insert them into the PostgreSQL database.
    """
    last_comments = get_last_comments()
    load_to_database(last_comments, hook)


default_args = {
    'depends_on_past': False,
    'start_date': days_ago(1),
}

with DAG(
        'long_track',
        default_args=default_args,
        description="A simple to DAG to fetch and load last movies' comments",
        schedule_interval='0/5 * * * *',
        catchup=False,
) as dag:

    create_comments_task = PostgresOperator(
        task_id="create_comments_table",
        sql="""CREATE TABLE IF NOT EXISTS comments (
                id SERIAL PRIMARY KEY,
                movie_id INTEGER NOT NULL,
                comment VARCHAR NOT NULL,
                rating INTEGER NOT NULL
            );""",
        postgres_conn_id='postgres_connection'
    )

    hook = PostgresHook(postgres_conn_id='postgres_connection')

    get_and_insert_last_comments_task = PythonOperator(
        task_id='get_and_insert_last_comments',
        python_callable=get_and_insert_last_comments,
        op_kwargs=dict(hook=hook),
    )

    create_comments_task >> get_and_insert_last_comments_task
