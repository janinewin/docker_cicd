import csv
import os
from csv import writer

import requests
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

AIRFLOW_HOME = os.getenv('AIRFLOW_HOME')


def create_file_if_not_exist(quotes_file: str) -> None:
    """
    Checks that the `quotes_file` exists and creates it otherwise.
    """
    if not os.path.isfile(quotes_file):
        with open(quotes_file, 'w'):
            return


def get_quote() -> str:
    """
    Calls https://breaking-bad.lewagon.com/v1/quotes
    and returns the 'quote' field of the answer.
    """
    return requests.get(
        "https://breaking-bad.lewagon.com/v1/quotes").json()['quote']


def is_quote_new(quotes_file: str, quote: str) -> bool:
    """
    Reads the `quote_file`and returns False if the `quote` is
    already inside. Returns True otherwise.
    """
    with open(quotes_file, 'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            if quote == row[0]:
                return False
    return True


def save_quote(quotes_file: str, quote: str) -> None:
    """
    Saves the `quote` in the `quotes_file`.
    """
    with open(quotes_file, 'a+') as file:
        csv_writer = writer(file)
        csv_writer.writerow([quote])


def get_quote_and_save_if_new(quotes_file: str) -> None:
    """
    Reuses the get_quote, is_quote_new and save_quote
    functions to get a quote and save it if it is a new one.
    """
    quote = get_quote()

    if is_quote_new(quotes_file, quote):
        save_quote(quotes_file, quote)


default_args = {'depends_on_past': False, 'start_date': days_ago(1)}

with DAG(
        'breaking_bad_quotes',
        default_args=default_args,
        description='A simple DAG to store breaking bad quotes',
        schedule_interval='0/5 * * * *',
        catchup=False,
) as dag:

    quotes_file = f'{AIRFLOW_HOME}/data/quotes.csv'

    create_file_if_not_exist_task = PythonOperator(
        task_id='create_file_if_not_exist',
        python_callable=create_file_if_not_exist,
        op_kwargs=dict(quotes_file=quotes_file),
    )

    get_quote_and_save_if_new_task = PythonOperator(
        task_id="get_quote_and_save_if_new",
        python_callable=get_quote_and_save_if_new,
        op_kwargs=dict(quotes_file=quotes_file),
    )

    create_file_if_not_exist_task >> get_quote_and_save_if_new_task
