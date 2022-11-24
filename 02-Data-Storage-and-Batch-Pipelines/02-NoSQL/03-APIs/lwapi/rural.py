import os
import pathlib

import pandas


def get_rural_csv_fp():
    """
    This function returns the path to the API-rural.CSV filepath. Feel free to use it to load the CSV file.
    """
    parent_dir = pathlib.Path(os.path.realpath(__file__)).parent.parent
    csv_fp = os.path.join(parent_dir, "data", "API-rural.csv")
    return csv_fp


def load_rural_csv():
    return pandas.read_csv(get_rural_csv_fp())
