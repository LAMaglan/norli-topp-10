import os.path
import requests
import json
import pandas as pd


class EmptyDataException(Exception):
    pass


def parse_wesbite(url=None, payload=None):
    response = requests.post(url, data=json.dumps(payload))

    if response.status_code != 200:
        raise EmptyDataException(
            f'''
            The HTTP response is {response.status_code},
            which might be an issue with runner on
            Github Actions
            '''
        )

    # Assuming response.content contains the JSON string,
    # convert the bytes to a string
    json_string = response.content.decode()  

    # Parse the JSON string
    return json.loads(json_string)


def parse_data(json_data):
    """ Get title and author details"""

    author_list = [hit["authors_name"] if isinstance(hit["authors_name"], list) 
                   else [hit["authors_name"]] for hit in json_data["results"][0]["hits"]]

    book_list = [hit["name"] for hit in json_data["results"][0]["hits"]]

    if not author_list or not book_list:
        raise EmptyDataException(
            "Something wrong with book or author lists (likely no data)")
    
    book_details = zip(author_list, book_list)

    book_details = pd.DataFrame(book_details, columns=['Author names', 'Book'])

    # remove square brackets from "Author names"
    book_details['Author names'] = book_details['Author names'].apply(', '.join)


    return book_details



def create_csv_file(book_details, old_file_exists, old_file, filepath):
    """Create csv-file from parsed webpage"""

    if not old_file_exists:
        book_details.to_csv(filepath, index=False)
    else:
        if not old_file.equals(book_details):
            book_details.to_csv(filepath, index=False)


def main(url=None, payload=None):
    """ Run all """
    output_filepath = "output/topp-10-norli.csv"

    if os.path.isfile(output_filepath):
        old_file_exists = True
        old_file = pd.read_csv(output_filepath)
    else:
        old_file_exists = False
        old_file = ""

    norli_data = parse_wesbite(url=url, payload=payload)

    book_details = parse_data(norli_data)
    
    create_csv_file(book_details, old_file_exists,
                    old_file, filepath=output_filepath)



if __name__ == "__main__":
    url = "https://aeeyieersj-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia for JavaScript (4.19.1); Browser (lite)&x-algolia-api-key=ZjRlODkxZDFhY2MyOTE1YWU1OGRjZTRlYjZlMTViZDkwNWNmYjE3YmU2MjU4YzhlOGZjZjg4MTc3ZDY4M2FjYnJlc3RyaWN0U291cmNlcz0xOTMuMTU3LjIwNy4xODkmdGFnRmlsdGVycz0=&x-algolia-application-id=AEEYIEERSJ"

    payload = {
        "requests":
            [
                {
                    "indexName":"norli_pwa_products","params":"clickAnalytics=true&facets=%5B%22format%22%2C%22authors_name%22%2C%22price.NOK.default%22%2C%22language%22%2C%22series%22%2C%22thema_subject%22%2C%22editionreleaseyear%22%2C%22color%22%2C%22number_of_pages%22%2C%22mammoth_number%22%2C%22categories.level0%22%5D&filters=categoryIds%3A5334&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&highlightPreTag=%3Cais-highlight-0000000000%3E&hitsPerPage=48&maxValuesPerFacet=50&page=0&tagFilters="
                }
            ]
        }
    
    main(url=url, payload=payload)