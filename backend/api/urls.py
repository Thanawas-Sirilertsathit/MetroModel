from django.urls import path
from .views import ProjectHourlyAverageAPIView, ProjectOnedayAverageAPIView, ProjectPredictionAPIView
urlpatterns = [
    path('hourly/', ProjectHourlyAverageAPIView.as_view(), name='hourly'),
    path('oneday/', ProjectOnedayAverageAPIView.as_view(), name='oneday'),
    path('predict/', ProjectPredictionAPIView.as_view(), name='predict'),
]
