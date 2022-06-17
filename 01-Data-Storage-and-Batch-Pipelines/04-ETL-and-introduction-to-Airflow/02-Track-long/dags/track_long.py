import os

from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook

# IMPORT YOUR PACKAGES HERE

AIRFLOW_HOME = os.getenv('AIRFLOW_HOME')
COMMENTS_API_ROOT = os.getenv("COMMENTS_API_ROOT", "http://dev.sapiologie.com:8008/latest-comments/")


def get_last_comments(number_of_comments: int) -> list:
    """
    Calls http://dev.sapiologie.com:8008/latest-comments/?n=number_of_comments to
    get the last `number_of_comments` comments
    and returns the 'comments' field of the answer.
    """
    pass  # YOUR CODE HERE


def double_single_quote(comment: str) -> str:
    """
    Returns the `comment` with all single quotes
    replaced by two single quotes (not a double quote).
    """
    pass  # YOUR CODE HERE


def load_to_database(comments: list, hook) -> None:
    """
    Iterates over the comments, uses double_single_quote function
    to clean each comment and loads them into
    the PostgreSQL database using the PostgresHook.
    (Note: It is not idempotent as it will insert the same comments if we
    trigger the same task twice, but this is what we want.)
    """
    pass  # YOUR CODE HERE


def get_and_insert_last_comments(hook: PostgresHook) -> str:
    """
    Uses get_last_comments and load_to_database functions to get
    the last five comments and insert them into the PostgreSQL database.
    """
    pass  # YOUR CODE HERE


with DAG(
        'track_long',
        # YOUR CODE HERE
) as dag:
    pass  # YOUR CODE HERE
