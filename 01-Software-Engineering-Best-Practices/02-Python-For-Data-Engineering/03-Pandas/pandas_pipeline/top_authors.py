import pandas as pd
from pathlib import Path


def write_author_impact_analysis(combined_df: pd.DataFrame, data_path: Path) -> None:
    """
    Generates a CSV file of the top 10 most impactful authors based on their average review score and number of reviews.

    Criteria:
    - Impact is calculated as a weighted sum of normalized review scores and normalized number of reviews.
    - The weighting for number of reviews is 0.8.
    - Missing authors are not considered in the analysis.
    - Brackets around author names are removed in the output.

    Parameters:
    - combined_df (pd.DataFrame): DataFrame resulting from the merge of ratings and book details.
    - data_path (Path): pathlib.Path object indicating where the result should be saved.

    Output File:
    - "author_impact_analysis.csv" saved in the specified `data_path`.

    Output Columns:
    - author: The name of the author.
    - average_review_score: The average score of reviews received by the author's books.
    - number_of_reviews: The total number of reviews received by the author's books.
    - impact_score: Calculated score based on normalized review scores and number of reviews (with a 0.8 weighting on reviews).

    Returns:
    - None: Writes the result to the specified path.
    """
    # $CHALLENGIFY_END
    combined_df = combined_df[
        combined_df["authors"].notna() & (combined_df["authors"] != "nan")
    ]

    author_impact = (
        combined_df.groupby("authors")
        .agg({"review/score": "mean", "User_id": "count"})
        .reset_index()
    )

    author_impact["authors"] = author_impact["authors"].str.replace(r"[\[\]']", "")
    author_impact.columns = ["author", "average_review_score", "number_of_reviews"]

    max_reviews = author_impact["number_of_reviews"].max()
    max_score = author_impact["average_review_score"].max()

    author_impact["normalized_review_score"] = (
        author_impact["average_review_score"] / max_score
    )
    author_impact["normalized_review_count"] = (
        author_impact["number_of_reviews"] / max_reviews
    )

    author_impact["impact_score"] = (
        0.2 * author_impact["normalized_review_score"]
        + 0.8 * author_impact["normalized_review_count"]
    )

    top_authors = author_impact.nlargest(10, "impact_score")[
        ["author", "average_review_score", "number_of_reviews", "impact_score"]
    ]
    top_authors["author"] = (
        top_authors["author"].str.strip("[]").str.replace("'", "").str.strip()
    )

    top_authors.to_csv(data_path / "author_impact_analysis.csv", index=False)
    # $CHALLENGIFY_BEGIN
