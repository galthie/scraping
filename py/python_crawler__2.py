from typing import Iterator  # 型ヒントのためにインポート
import requests
import lxml.html


def main():
    """
    クローラーのメインの処理。
    """
    response = requests.get('https://gihyo.jp/dp')
    # scrape_list_page()関数を呼び出し、ジェネレーターイテレーターを取得する。
    urls = scrape_list_page(response)
    for url in urls:  # ジェネレーターイテレーターはlistなどと同様に繰り返し可能。
        print(url)


def scrape_list_page(response: requests.Response) -> Iterator[str]:
    """
    一覧ページのResponseから詳細ページのURLを抜き出すジェネレーター関数。
    """
    html = lxml.html.fromstring(response.text)
    html.make_links_absolute(response.url)

    for a in html.cssselect('#listBook > li > a[itemprop="url"]'):
        url = a.get('href')
        yield url  # yield文でジェネレーターイテレーターの要素を返す。

if __name__ == '__main__':
    main()
