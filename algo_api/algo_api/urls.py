from django.urls import path

from algo_api import views

urlpatterns = [
    path('forecast/<str:ticker>', views.get_forecast),
]
