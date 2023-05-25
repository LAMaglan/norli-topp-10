import os.path
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import pandas as pd


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


def create_csv_file(author_list, book_list, old_file_exists, old_file, filepath):
    """Create csv-file from parsed webpage"""
    data = {"author": author_list, "title": book_list,
            "rank": list(range(1, len(book_list)+1))}

    data_pd = pd.DataFrame.from_dict(data)

    if not old_file_exists:
        data_pd.to_csv(filepath, index=False)
    else:
        if not old_file.equals(data_pd):
            data_pd.to_csv(filepath, index=False)


def main():
    """ Run all """
    output_filepath = "output/topp-10-norli.csv"

    if os.path.isfile(output_filepath):
        old_file_exists = True
        old_file = pd.read_csv(output_filepath)
    else:
        old_file_exists = False
        old_file = ""

    driver = webdriver.Chrome(options=set_chrome_options())

    url = "https://www.norli.no/boker/aktuelt-og-anbefalt/topplister/topp-10-boker"
    driver.get(url)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    author_list, book_list = parse_webpage(soup)

    create_csv_file(author_list, book_list, old_file_exists,
                    old_file, filepath=output_filepath)

    driver.close()


if __name__ == "__main__":
    main()
