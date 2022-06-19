# IMPORT YOUR PACKAGES HERE

AIRFLOW_HOME = os.getenv("AIRFLOW_HOME")


def create_connection_from_hook(hook: Union[SqliteHook, PostgresHook]) -> Union[Engine, Connection]:
    """
    Creates a database connection from a PostgresHook/SqliteHook.
    """
    pass  # YOUR CODE HERE


def load_to_database(input_file: str, hook: PostgresHook, task_instance: TaskInstance):
    """
    Uses pandas functions to create a DataFrame from a parquet file and append it to the
    database. Uses xcom_push to export the number of inserted values (under the key `number_of_inserted_rows`).
    """
    pass  # YOUR CODE HERE


def display_number_of_inserted_rows(task_instance: TaskInstance):
    """
    Uses xcom_pull to get the number of inserted values to database and log it.
    """
    pass  # YOUR CODE HERE


with DAG(
    "load",
    # YOUR CODE HERE
) as dag:
    pass  # YOUR CODE HERE
