import os
import random
from typing import List


def datasets_dir():
    """
    Returns the datasets directory
    """
    return os.environ.get("DATASETS_DIR", "/datasets/")


def count_lines(fp: str):
    """
    Counts the number of lines in a file
    """
    n = 0
    with open(fp) as f:
        for _ in f:
            n += 1
    return n


def fetch_random_lines(n: int, total: int, fp: str) -> List[str]:
    """
    Fetches `n` lines at random from the text file at path `fp`, which has a total of `total` lines.
    The idea is to be smart with seeking the file in a sorted order and not load the file in memory to keep RAM usage minimal.
    """
    # Get a sorted sample of `n` line numbers
    line_numbers = sorted([random.randint(0, total - 1) for _ in range(n)])
    # Compute the distances (jumps) from one line to the next
    jumps = [line_numbers[0]]
    for prev_val, new_val in zip(line_numbers[0:-1], line_numbers[1:]):
        jumps.append(new_val - prev_val)

    # Skip every `jump - 1` value in the file and keep the `jump`'th
    values = []
    with open(fp) as f:
        for jump in jumps:
            for _ in range(max(0, jump - 1)):
                next(f)
            values.append(next(f))

    return values


def fetch_consecutive_lines(n: int, start: int, fp: str) -> List[str]:
    """
    Fetches `n` lines after `start` skipped lines
    """
    values = []
    with open(fp) as f:
        for _ in range(start):
            next(f)
        for _ in range(max(0, n)):
            values.append(next(f))

    return values


def random_rating(sentiment: str):
    """
    The dataset returns `"positive"` or `"negative"`, we associate ratings of 1 or 2 for negative reviews, 3, 4, 5 otherwise.
    """
    options = [1, 2] if sentiment == "negative" else [3, 4, 5]
    return random.choice(options)


def get_comment_sentiment_from_row(row: str):
    """
    The sentiment is at the end of the CSV, either "positive" or "negative" (both 8 characters long)
    """
    sentiment = row[-8:]
    comment = row[1:-11]
    return comment, sentiment
