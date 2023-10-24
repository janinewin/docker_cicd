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
    df = combined_df[["Title", "review/score", "ratingsCount", "authors"]].rename({"Title": "title", "review/score": "average_review_score", "ratingsCount": "number_of_reviews", "authors": "author"}, axis=1)
    print(df.head())
    df = df.query("number_of_reviews >= 25")

    #df["author"] = [", ".join(map(str, l)) for l in df["authors"]]

    #df.rename(columns={"Title": "title", "review/score": "average_review_score", "ratingsCount": "number_of_reviews", "authors": "author"}, inplace=True)
    #print(df.head())
    df = df[["title", "average_review_score", "number_of_reviews", "author"]].groupby(["title", "number_of_reviews", "author"]).mean()
    #df = df[["Title", "review/score", "ratingsCount", "authors"]].groupby(["Title", "ratingsCount", "authors"]).mean()
    print(df.head())
    #df = df.reset_index(drop=True)
    #df = df.astype({"authors": str})
    #df.replace(["[", "]"], "")

    #df.groupby(["title", "number_of_reviews", "author"]).mean()
    #df = df.drop_duplicates()

    df = df.sort_values("average_review_score", ascending=False)
    df = df[["title", "average_review_score", "number_of_reviews", "author"]]
    print(df.head())
    df = df.head(10)
    #df = df[["title", "average_review_score", "number_of_reviews", "author"]]

    df.to_csv(data_path + "/best_performing_books.csv") #, index=False)


if __name__ == "__main__":
    df = load.load_data("./data")
    write_best_performing_books(df, "./data")
