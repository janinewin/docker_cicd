import os

from airflow import DAG

# IMPORT YOUR PACKAGES HERE

AIRFLOW_HOME = os.getenv("AIRFLOW_HOME")


def create_file_if_not_exist(quotes_file: str) -> None:
    """
    Creates the `quotes_file` if it doesn't exists, does nothing
    otherwise.
    """
    pass  # YOUR CODE HERE


def get_quote() -> str:
    """
    Calls https://breaking-bad.lewagon.com/v1/quotes
    and returns the 'quote' field of the answer.
    """
    pass  # YOUR CODE HERE


def is_quote_new(quotes_file: str, quote: str) -> bool:
    """
    Reads the `quote_file`and returns False if the `quote` is
    already inside. Returns True otherwise.
    """
    pass  # YOUR CODE HERE


def save_quote(quotes_file: str, quote: str) -> None:
    """
    Saves the `quote` in the `quotes_file`.
    """
    pass  # YOUR CODE HERE


def get_quote_and_save_if_new(quotes_file: str) -> None:
    """
    Reuses the get_quote, is_quote_new and save_quote
    functions to get a quote and save it if it is a new one.
    """
    pass  # YOUR CODE HERE


with DAG(
    "breaking_bad_quotes",
    # YOUR CODE HERE
) as dag:
    pass  # YOUR CODE HERE
