import pandas as pd
import pathlib
from pandas_pipeline.utils import timing

DATA_PATH = pathlib.Path(__file__).parent.parent / "data"


@timing
def load_data(row_count=1000) -> pd.DataFrame:
    books = pd.read_csv(DATA_PATH / "books_data.csv", nrows=row_count)
    ratings = pd.read_csv(DATA_PATH / "Books_rating.csv", nrows=row_count)
    return books, ratings


@timing
def load_data_pyarrow() -> pd.DataFrame:
    books = pd.read_csv(DATA_PATH / "books_data.csv", engine="pyarrow")
    ratings = pd.read_csv(DATA_PATH / "Books_rating.csv", engine="pyarrow")
    return books, ratings


if __name__ == "__main__":
    load_data(row_count=None)
    load_data_pyarrow()
