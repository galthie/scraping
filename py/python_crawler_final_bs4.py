import re
import time
from typing import Iterator
import requests
import lxml.html
from pymongo import MongoClient
from urllib.parse import urljoin
from bs4 import BeautifulSoup


def main():
    client = MongoClient('localhost', 27017)
    collection = client.scraping.ebooks
    collection.create_index('key', unique=True)

    session = requests.Session()
    response = session.get('https://gihyo.jp/dp')
    urls = scrape_list_page(response)
    for url in urls:
        key = extract_key(url)

        ebook = collection.find_one({'key': key}) 
        if not ebook:
            time.sleep(1)
            response = session.get(url)
            ebook = scrape_detail_page(response)
            collection.insert_one(ebook)

        print(ebook)
    

def scrape_list_page(response: requests.Response) -> Iterator[str]:
    soup = BeautifulSoup(response.text, 'html.parser')

    for a in soup.select('#listBook > li > a[itemprop="url"]'):
        url = a.get('href')
        yield url


def scrape_detail_page(response: requests.Response) -> dict:
    soup = BeautifulSoup(response.text, 'html.parser')
    ebook = {
        'url': response.url,
        'title': html.cssselect('#bookTitle')[0].text_content(),
        'price': html.cssselect('.buy')[0].text.strip(),
        'content': [normalize_spaces(h3.text_content()) for h3 in html.cssselect('#content > h3')],
    }
    return ebook


def extract_key(url: str) -> str:
    m = re.search(r'/([^/]+)$', url)
    return m.group(1)


def normalize_spaces(s: str) -> str:
    return re.sub(r'\s+', ' ',s).strip()


if __name__ == '__main__':
    main()
