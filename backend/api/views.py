from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import SampleDataSerializer, ProjectSerializer
from .models import Project

class SampleDataView(APIView):
    def get(self, request):
        data = {"message": "I am Rest API!"}
        serializer = SampleDataSerializer(data)
        return Response(serializer.data)

class ProjectListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)
