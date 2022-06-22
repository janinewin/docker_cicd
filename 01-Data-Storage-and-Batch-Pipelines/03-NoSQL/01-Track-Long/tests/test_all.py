import os
import pathlib


def test_csv():
    parent_dir = pathlib.Path(os.path.realpath(__file__)).parent.parent
    movies_csv_fp = os.path.join(parent_dir, "data", "movies_metadata.csv")
    assert os.path.isfile(movies_csv_fp), "file movies_metadata.csv not found under data/"
