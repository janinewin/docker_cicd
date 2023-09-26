# Scraping

🏁 The goal for today is to setup a process which

1. scrapes stories from [hackernews](https://news.ycombinator.com/front)
2. Uploads them to our lake
3. Verifies the data quality
4. Transforms the data
5. Allows scoped access to the data

The first challenge will be about scraping the data we will use beautiful soup for this!


## Introduction to Web Scraping

Web scraping is the process of extracting data from websites. This involves making requests to websites and then parsing the returned HTML to extract the desired data.

## BeautifulSoup

🍜 [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) is a Python library widely used for web scraping purposes. It parses HTML and XML documents and extracts data in a hierarchical and readable manner.

### Basic Example with BeautifulSoup

Consider the following scenario: You want to extract the title of a Wikipedia page.

```python
import requests
from bs4 import BeautifulSoup

URL = "https://en.wikipedia.org/wiki/Web_scraping"
response = requests.get(URL)
soup = BeautifulSoup(response.content, 'html.parser')
title = soup.title.text
print(title)  # Outputs: Web scraping - Wikipedia
```


## Step by step challenge ❓

### 1. Setting up the scraper function:

   a. In the `scrape.py` file, initialize the `scrape_hn(date: str) -> pd.DataFrame` function.

   b. Make a GET request to the HN website to retrieve the top stories for the given date.

   c. Check the response status. If it's not 200 (HTTP OK), handle the error gracefully.

   > 💡 **Hint**: Use the `requests` library for making HTTP requests. Remember to check the status code of the response to ensure the request was successful.

### 2. Parsing the HTML:

   a. Use BeautifulSoup to parse the returned HTML.

   b. Locate the relevant HTML elements containing story details, like titles, links, and author names.

   c. Extract the data and store it in an appropriate data structure, such as a list of dictionaries.

   > 💡 **Hint**: You can use the browser's developer tools to inspect the HTML structure of the Hacker News website. This will help you identify the tags and classes containing the desired information.

### 3. Saving to CSV:

   a. Convert the list of dictionaries into a pandas DataFrame.

   b. In the `main.py` file, call the `scrape_hn` function to fetch the data for the current date.

   c. Save the DataFrame to a CSV file named "stories.csv".

   > 💡 **Hint**: Pandas provides a convenient `to_csv` method to save DataFrames to CSV files. Remember to set `index=False` to avoid saving the DataFrame index to the CSV.

### 4. Error Handling:

   a. Ensure your scraper handles exceptions gracefully, such as missing elements or network errors.

   b. Consider adding retries or delays to respect the website's terms and prevent overloading it.

   > 💡 **Hint**: The `try` and `except` blocks in Python can be used to catch and handle exceptions. You can catch specific exceptions (like `requests.exceptions.RequestException`) to handle known issues.

## 🏁 Completion

Once you are done with the challenge, you can run the following command to check your code:

```bash
make test
```

If it passes you can push to git! Now you are extracting `stories.csv` from HN you are ready to move on and begin uploading the data to our lake!
