import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape_hn(date: str) -> pd.DataFrame:
    """
    Scrape the daily top stories from Hacker News (HN) for a specified date.

    Parameters:
    - date (str): The desired date for which to scrape the top stories.
                  Format should be "YYYY-MM-DD".

    Returns:
    - pd.DataFrame: A DataFrame containing details of the top stories including:
        - rank (int): The ranking of the story on HN.
        - title (str): The title of the story.
        - site (str): The site domain from where the story is sourced.
        - link (str): The direct link to the story.
        - score (int): The total score (or upvotes) the story has received.
        - author (str): The name of the user who posted the story.
        - comments_number (int): The number of comments the story has.
                                Defaults to 0 if not present.

    Raises:
    - Exits the program with a message if the response status code from HN is not 200.

    """
    pass  # YOUR CODE HERE
