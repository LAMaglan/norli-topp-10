from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import pandas as pd

url = "https://www.norli.no/boker/aktuelt-og-anbefalt/topplister/topp-10-boker"


def set_chrome_options() -> Options:
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options


def parse_webpage(soup):
    """ Get title and author details"""

    all_books = soup.find_all("a", class_="itemNorli-name-2Vz")
    all_authors = soup.find_all("div", class_="itemNorli-authorName-1ZR")

    author_list = []
    for author in all_authors:
        author_list.append(author.get_text())

    book_list = []
    for book in all_books:
        book_list.append(book.get_text())

    return author_list, book_list


def create_csv_file(author_list, book_list):
    """Create csv-file from parsed webpage"""
    data = {"author": author_list, "title": book_list,
            "rank": list(range(1, len(book_list)+1))}

    data_pd = pd.DataFrame.from_dict(data)

    data_pd.to_csv('output/topp-10-norli.csv', index=False)


def main():
    """ Run all """
    driver = webdriver.Chrome(options=set_chrome_options())

    driver.get(url)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    author_list, book_list = parse_webpage(soup)
    create_csv_file(author_list, book_list)

    driver.close()


if __name__ == "__main__":
    main()
