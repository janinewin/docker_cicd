import pandas as pd
from pathlib import Path
import load


def write_best_performing_books(combined_df: pd.DataFrame, data_path: Path) -> None:
    """
    Generates a CSV file of the top 10 best performing books based on their average review score.

    Criteria:
    - Books should have at least 25 reviews.
    - Removes any surrounding brackets from the author names.

    Parameters:
    - combined_df (pd.DataFrame): DataFrame resulting from the merge of ratings and book details.
    - data_path (Path): pathlib.Path object indicating where the result should be saved.

    Output File:
    - "best_performing_books.csv" saved in the specified `data_path`.

    Output Columns:
    - title: The title of the book.
    - average_review_score: The average score of reviews received by the book.
    - number_of_reviews: The total number of reviews received by the book.
    - author: The author(s) of the book, with any surrounding brackets removed.

    Returns:
    - None: Writes the result to the specified path.
    """
    df = combined_df[["Title", "authors", "review/score"]].rename({"Title": "title"}, axis=1)

    df["number_of_reviews"] = 1
    df = df.groupby(["title", "authors"], as_index=False).sum()
    df["average_review_score"] = df["review/score"] / df["number_of_reviews"]

    df = df[(df.number_of_reviews >= 25)]
    df = df.sort_values(["average_review_score", "number_of_reviews"], ascending=False)
    df = df.head(50)

    df["author"] = df["authors"].str.replace("[", "")
    df["author"] = df["author"].str.replace("]", "")

    df[["title", "average_review_score", "number_of_reviews", "author"]].to_csv(data_path + "/best_performing_books.csv", index=False)



if __name__ == "__main__":
    df = load.load_data("./data")
    write_best_performing_books(df, "./data")
