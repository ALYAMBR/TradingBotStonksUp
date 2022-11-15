import requests

API_URL = 'localhost:5000'


def api_get_prediction(ticker: str, date: str) -> requests.Response:
    return requests.get(f'{API_URL}/forecast/' + ticker, params={'date': date})
