from scraper.scrape import scrape_hn
from datetime import datetime


def main():
    date_today = datetime.now().strftime("%Y-%m-%d")
    stories_df = scrape_hn(date_today)
    stories_df.to_csv("stories.csv", index=False)


if __name__ == "__main__":
    main()
