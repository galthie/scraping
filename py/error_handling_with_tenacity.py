import requests
from tenacity import retry, stop_after_attempt, wait_exponential

TEMPORARY_ERROR_CODES = (408, 500, 502, 503, 504)


def main():
    response = fetch('http://httpbin.org/status/200,404,503')
    if 200 <= response.status_code < 300:
        print('Success!')
    else:
        print('Error!')

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1))
def fetch(url: str) -> requests.Response:
    print(f'Retrieving {url}...')
    response = requests.get(url)
    print(f'Status: {response.status_code}')
    if response.status_code not in TEMPORARY_ERROR_CODES:
        return response


    raise Exception(f'Temporary Error: {response.status_code}')


if __name__ == '__main__':
    main()
