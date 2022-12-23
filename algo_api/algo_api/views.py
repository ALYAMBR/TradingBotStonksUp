import os
import requests
import pandas
from pipeline import Pipeline


from dateutil import parser
from django.http import JsonResponse

MODELS_FOLDER = "models"
TIMEFRAME = "1H"
WINDOW_LENGTH = 5
MOEX_BACKEND_URL = "http://moex:8080"
FROM = '2021-09-01T00:00:00'
TILL = '2021-09-03T00:00:00'


def get_forecast(request, ticker):
    date = request.GET.get('date')
    algorithm_name = request.GET.get("algorithmName")
    exchange_name = request.GET.get("exchangeName")
    print(ticker, date, algorithm_name, exchange_name)
    data = get_stocking_data(ticker, TIMEFRAME, exchange_name)
    df = make_csv_data(data)
    growth_chance = get_prediction(df, algorithm_name, exchange_name, ticker)
    response = {
        'growthChange': growth_chance
    }
    return JsonResponse(response)


def get_prediction(data_frame, algorithm_name, exchange_name, ticker):
    model_path = os.path.join("algo_api", MODELS_FOLDER, f"{ticker}-{TIMEFRAME}-{WINDOW_LENGTH}.pickle")
    pipeline = Pipeline.load(model_path)
    value = pipeline.predict(data_frame)
    return value


def get_stocking_data(ticker, timeframe, exchange_name):
    params = {
        'exchangeName': exchange_name,
        'timeframe': 60,
        'till': TILL,
        'from': FROM
    }
    url = MOEX_BACKEND_URL + '/data/' + ticker
    response = requests.get(url, params=params)
    data = response.json()
    return data


def make_csv_data(data):
    bargainings = convert_date_type(data['bargainings'])
    columns = ['<TICKER>', '<PER>', '<DATE>', '<TIME>', '<OPEN>', '<HIGH>', '<LOW>', '<CLOSE>', '<VOL>']
    df = pandas.DataFrame(bargainings, columns=columns)
    return df


def convert_date_type(old_bargainings):
    converted_bargainings = []
    for bargaining in old_bargainings:
        datetime = parser.parse(bargaining['date'])
        date = datetime.date()
        time = datetime.time()
        converted_bargaining = [bargaining['ticker'], bargaining['per'], date, time, bargaining['open'], bargaining['high'], bargaining['low'], bargaining['close'], bargaining['vol']]

        converted_bargainings.append(converted_bargaining)
    return converted_bargainings