import random

from django.http import JsonResponse


def get_forecast(request, ticker):
    date = request.GET.get('date')
    algorithm_name = request.GET.get("algorithmName")
    exchange_name = request.GET.get("exchangeName")
    print(ticker, date, algorithm_name, exchange_name)
    growth_chance = random.random()
    response = {
        'growthChange': growth_chance
    }
    return JsonResponse(response)
