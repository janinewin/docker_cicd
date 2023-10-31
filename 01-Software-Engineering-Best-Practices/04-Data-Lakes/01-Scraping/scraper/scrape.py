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
    url = "https://news.ycombinator.com/front?day=" + date
    response = requests.get(url)
    if response.status_code != 200:
        print("There has been an Error while requesting the website.")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    result = pd.DataFrame(columns=["rank", "title", "site", "link", "score", "author", "comments_number"])

    titles = soup.findAll(name="tr", class_="athing")
    scores = soup.findAll(name="td", class_="subtext")

    for i, title in enumerate(titles):
        rank = i+1
        ttl = title.find("span", {"class": "titleline"}).a.text
        site = title.find("span", {"class": "sitestr"}).text
        link = title.find("span", {"class": "titleline"}).a["href"]
        score = int(scores[i].find("span", {"class": "score"}).text.replace(" points", ""))
        author = scores[i].find("a", {"class": "hnuser"}).text
        try: cmts_number = int(scores[i].find_all("a")[-1].text.replace("comments", ""))
        except: cmts_number = 0
        #if scores[i].find_all("a")[-1].text == "discuss": cmts_number = 0
        #else: cmts_number = int(scores[i].find_all("a")[-1].text.replace("comments", ""))

        new_row = {"rank": rank, "title": ttl, "site": site , "link": link, "score": score, "author": author, "comments_number": cmts_number}

        result = result.append(new_row, ignore_index=True)

    return result

if __name__ == "__main__":
    scrape_hn("2023-10-30")
