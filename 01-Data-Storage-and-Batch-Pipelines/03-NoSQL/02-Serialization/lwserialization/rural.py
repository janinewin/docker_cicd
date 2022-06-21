import os
import pathlib

# Import pandas
# IMPORT YOUR PACKAGES HERE

# Import the parquet library/ies
# IMPORT YOUR PACKAGES HERE


def get_rural_csv_fp():
    """
    This function returns the path to the API-rural.CSV filepath. Feel free to use it to load the CSV file.
    """
    parent_dir = pathlib.Path(os.path.realpath(__file__)).parent.parent
    csv_fp = os.path.join(parent_dir, "data", "API-rural.csv")
    return csv_fp


def load_rural_csv():
    pass  # YOUR CODE HERE


def explore_columns():
    # Add n_columns = <your answer>
    pass  # YOUR CODE HERE
    return n_columns


def explore_size():
    # Add size = <your answer>
    pass  # YOUR CODE HERE
    return size


def explore_countries():
    # Add countries = <your answer>
    pass  # YOUR CODE HERE
    return countries


def dataframe_to_parquet(dataframe, file_path: str):
    """
    Args:
        - dataframe: a pandas.DataFrame
        - file_path: a string, the file path to store the Parquet file to
    """
    assert file_path.endswith(".parquet")
    pass  # YOUR CODE HERE


def load_dataset_and_convert_to_parquet():
    pass  # YOUR CODE HERE
