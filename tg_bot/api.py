import requests

STOCKS_API_URL = 'http://localhost:8080'
PREDICTION_API_URL = 'http://localhost:8000'


def api_get_stocks(page: int = 1, prefix: str = None) -> requests.Response:
    return requests.get(f'{STOCKS_API_URL}/stocks', params={'page': page, 'query': prefix})


def api_get_prediction(ticker: str, date: str) -> requests.Response:
    return requests.get(f'{PREDICTION_API_URL}/forecast/' + ticker, params={'date': date, 'exchangeName': 'MOEX'})
