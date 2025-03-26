from django.urls import path
from .views import SampleDataView, ProjectHourlyAverageAPIView

urlpatterns = [
    path('sample/', SampleDataView.as_view(), name='sample-data'),
    path('hourly/', ProjectHourlyAverageAPIView.as_view(), name='hourly'),
]
