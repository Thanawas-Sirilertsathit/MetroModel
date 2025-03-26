from django.urls import path
from .views import SampleDataView, ProjectListAPIView

urlpatterns = [
    path('sample/', SampleDataView.as_view(), name='sample-data'),
    path('projects/', ProjectListAPIView.as_view(), name='project-list'),
]
