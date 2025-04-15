from django.urls import path
from .views import SampleDataView, ProjectHourlyAverageAPIView, ProjectOnedayAverageAPIView
urlpatterns = [
    path('sample/', SampleDataView.as_view(), name='sample-data'),
    path('hourly/', ProjectHourlyAverageAPIView.as_view(), name='hourly'),
    path('oneday/', ProjectOnedayAverageAPIView.as_view(), name='oneday'),
]
