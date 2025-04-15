from django.urls import path
from .views import SampleDataView, ProjectHourlyAverageAPIView, ProjectOnedayAverageAPIView
from .views_weather import MergedWeatherAPIView
urlpatterns = [
    path('sample/', SampleDataView.as_view(), name='sample-data'),
    path('hourly/', ProjectHourlyAverageAPIView.as_view(), name='hourly'),
    path('oneday/', ProjectOnedayAverageAPIView.as_view(), name='oneday'),
        path('hourly-merged/', MergedWeatherAPIView.as_view(), name='hourly-merged'),
]
