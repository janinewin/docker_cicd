import pandas as pd
import requests_mock
from scraper.scrape import scrape_hn


def test_scrape_hn():
    with open(f"tests/test_html.txt", "r", encoding="utf-8") as f:
        mocked_html = f.read()

    with requests_mock.Mocker() as m:
        m.get("https://news.ycombinator.com/front?day=2023-09-20", text=mocked_html)

        df = scrape_hn("2023-09-20")

        assert isinstance(
            df, pd.DataFrame
        ), "Expected the result to be an instance of pandas DataFrame"
        assert df.shape[0] == 30, "Expected 2 stories in the DataFrame"

        assert df.iloc[0]["rank"] == 1, "Expected rank of the first story to be 1"
        assert (
            df.iloc[0]["title"] == "Story 1"
        ), "Expected title of the first story to be 'Story 1'"
        assert (
            df.iloc[0]["site"] == "example.com"
        ), "Expected site of the first story to be 'example.com'"
        assert (
            df.iloc[0]["link"] == "https://example.com/story1"
        ), "Expected link of the first story to be 'https://example.com/story1'"
        assert df.iloc[0]["score"] == 100, "Expected score of the first story to be 100"
        assert (
            df.iloc[0]["author"] == "User1"
        ), "Expected author of the first story to be 'User1'"
        assert (
            df.iloc[0]["comments_number"] == 50
        ), "Expected number of comments for the first story to be 50"

        assert df.iloc[1]["rank"] == 2, "Expected rank of the second story to be 2"
        assert (
            df.iloc[1]["title"] == "Story 2"
        ), "Expected title of the second story to be 'Story 2'"
        assert (
            df.iloc[1]["site"] == "example2.com"
        ), "Expected site of the second story to be 'example2.com'"
        assert (
            df.iloc[1]["link"] == "https://example.com/story2"
        ), "Expected link of the second story to be 'https://example.com/story2'"
        assert df.iloc[1]["score"] == 50, "Expected score of the second story to be 50"
        assert (
            df.iloc[1]["author"] == "User2"
        ), "Expected author of the second story to be 'User2'"
        assert (
            df.iloc[1]["comments_number"] == 0
        ), "Expected number of comments for the second story to be 0"
