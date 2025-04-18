from django.urls import path
from .views import ProjectHourlyAverageAPIView, ProjectOnedayAverageAPIView, ProjectPredictionAPIView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('hourly/', ProjectHourlyAverageAPIView.as_view(), name='hourly'),
    path('oneday/', ProjectOnedayAverageAPIView.as_view(), name='oneday'),
    path('predict/', ProjectPredictionAPIView.as_view(), name='predict'),
]
