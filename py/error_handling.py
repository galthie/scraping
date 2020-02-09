import time

import requests

TEMPORARY_ERROR_CODES = (408, 500, 502, 503, 504)


def main():
    response = fetch('http://httpbin.org/status/200,404,503')
    if 200 <= response.status_code < 300:
        print('Success!')
    else:
        print('Error!')


def fetch(url: str) -> requests.Response:
    max_retries = 3
    retries = 0
    while True:
        try:
            print(f'Retrieving {url}...')
            response = requests.get(url)
            print(f'Status: {response.status_code}')
            if response.status_code not in TEMPORARY_ERROR_CODES:
                return response

        except requests.exceptions.RequestException as ex:
            print(f'Network-level exception occured: {ex}')

        retries += 1
        if retries >= max_retries:
            raise Exception('Too many retries.')

        wait = 2**(retries -1)
        print(f'Waiting {wait} seconds...')
        time.sleep(wait)

if __name__ == '__main__':
    main()
