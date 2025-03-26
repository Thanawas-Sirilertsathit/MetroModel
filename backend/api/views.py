from django.db.models import Avg
from django.db.models.functions import TruncHour
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import SampleDataSerializer, ProjectSerializer
from .models import Project

class SampleDataView(APIView):
    def get(self, request):
        data = {"message": "I am Rest API!"}
        serializer = SampleDataSerializer(data)
        return Response(serializer.data)

class ProjectHourlyAverageAPIView(APIView):
    def get(self, request, *args, **kwargs):
        hourly_data = (
            Project.objects
            .annotate(hour=TruncHour('ts'))
            .values('hour')  # Grouping key
            .annotate(
                lat=Avg('lat'),
                lon=Avg('lon'),
                humid=Avg('humidity'),
                pressure=Avg('pressure'),
                temp=Avg('temperature')
            )
            .order_by('hour')
        )

        return Response(hourly_data)
