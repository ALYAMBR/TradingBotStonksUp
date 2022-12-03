import requests

API_URL = 'http://localhost:8080/api/v1'


def api_get_stocks(page: int = 1) -> requests.Response:
    return requests.get(f'{API_URL}/stocks', params={'page': page})


def api_get_prediction(ticker: str, date: str) -> requests.Response:
    return requests.get(f'{API_URL}/forecast/' + ticker, params={'date': date})
