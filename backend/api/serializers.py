from rest_framework import serializers
from .models import Project

class SampleDataSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=200)

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
