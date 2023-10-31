from scraper.scrape import scrape_hn
from datetime import datetime


def main():
    """
    Call the scrape_hn() function to fetch data for the current date and save to stories.csv
    """
    # $CHALLENGIFY_BEGIN
    date_today = datetime.now().strftime("%Y-%m-%d")
    stories_df = scrape_hn(date_today)
    stories_df.to_csv("stories.csv", index=False)
    # CHALLENGIFY_END

if __name__ == "__main__":
    main()
