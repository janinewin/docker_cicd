from pathlib import Path
import pandas as pd


def load_data(data_path: Path) -> pd.DataFrame:
    """
    Loads books data and ratings data from the specified path and returns a combined DataFrame.

    Parameters:
    - data_path (Path): Path to the directory containing the "books_data.csv" and "Books_rating.csv" files.

    Returns:
    - combined_df (pd.DataFrame): A DataFrame resulting from the inner merge of books data and ratings data on the "Title" column.

    Note:
    - "books_data.csv" should contain book details.
    - "Books_rating.csv" should contain book ratings.
    - Both CSVs are expected to have a "Title" column for the merge operation.
    - An inner merge is performed, so only books that exist in both datasets will be included in the result.

    Raises:
    - FileNotFoundError: If either of the CSV files is missing in the specified path.
    """
    try:
        dt_df = pd.read_csv(data_path + "/books_data.csv")
        print("books_data loaded")
        rt_df = pd.read_csv(data_path + "/Books_rating.csv")
        print("books_rating loaded")
        combined_df = pd.merge(dt_df, rt_df, "inner", "Title")
        print("df merged")
        #print(combined_df.info())
        return combined_df
    except FileNotFoundError:
        print("One or both files are missing ..")




if __name__ == "__main__":
    load_data("./data")
