import csv
import os
from typing import List
import uuid

from fastapi import FastAPI

from moviecomment import models
from moviecomment import helper

DEFAULT_N = 10
FN_MOVIE_IDS = "movie_ids.csv"
FN_COMMENTS = "imdb_comments_dataset.csv"
MAX_N = 50


def load_settings():
    """
    Loads shared settings in the app object directly, for easy reuse throughout the calls
    """
    movies_fp = os.path.join(helper.datasets_dir(), FN_MOVIE_IDS)
    comments_fp = os.path.join(helper.datasets_dir(), FN_COMMENTS)

    return models.Settings(
        n_movies=helper.count_lines(movies_fp),
        n_comments=helper.count_lines(comments_fp),
        movies_fp=movies_fp,
        comments_fp=comments_fp,
    )


app = FastAPI()
app.settings = load_settings()
print(f"Loaded settings {app.settings}")


def new_comments(n: int = DEFAULT_N) -> List[models.Comment]:
    """ """
    movie_ids_str = helper.fetch_random_lines(
        n=n, total=app.settings.n_movies, fp=app.settings.movies_fp
    )
    comments_str = helper.fetch_random_lines(
        n=n, total=app.settings.n_comments, fp=app.settings.comments_fp
    )

    comments = []
    for movie_id_str, comment_row_str in zip(movie_ids_str, comments_str):
        comment, sentiment = helper.get_comment_sentiment_from_row(comment_row_str)
        rating = helper.random_rating(sentiment)
        comments.append(
            models.Comment(movie_id=int(movie_id_str), comment=comment, rating=rating)
        )
    return comments


@app.get("/latest-comments")
async def latest_comments(n: int = DEFAULT_N) -> models.LatestCommentsResponse:
    """
    API endpoints returning a JSON of `n` latest comments
    """
    n = max(1, min(n, MAX_N))
    return models.LatestCommentsResponse(comments=new_comments(n=n))


@app.get("/dump-csv")
async def dump_csv(n: int):
    """
    API endpoints returning a JSON of `n` latest comments
    """
    fp = f"/tmp/{uuid.uuid4()}.csv"

    with open(fp, "w") as f:
        fieldnames = ["id", "movie_id", "rating", "comment"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        idx = 1
        for _ in range(n // DEFAULT_N):
            comments: List[models.Comment] = new_comments(DEFAULT_N)
            for comment in comments:
                writer.writerow(
                    {
                        "id": idx,
                        "movie_id": comment.movie_id,
                        "comment": comment.comment,
                        "rating": comment.rating,
                    }
                )
                idx += 1

    return {"fp": fp}
