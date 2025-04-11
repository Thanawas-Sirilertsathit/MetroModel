import pandas as pd
from django.db.models import Avg
from django.db.models.functions import TruncHour
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import SampleDataSerializer, ProjectSerializer
from .models import Project
from datetime import datetime, time
from .model_registry import model_collection
from .utils import get_time_block, format_json_output

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
            .values('hour')
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


class ProjectOnedayAverageAPIView(APIView):
    def get(self, request, *args, **kwargs):
        date_str = request.query_params.get('date')
        key = request.query_params.get('key')
        if not date_str or not key:
            return Response({'error': 'Missing required parameters: date and key for organization'}, status=400)
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return Response({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=400)
        try:
            key = int(key)
        except ValueError:
            return Response({'error': 'Key must be an integer.'}, status=400)

        if key in [1, 2, 3, 4, 8]:
            start_hour = 5
        elif key in [5, 6, 7]:
            start_hour = 6
        else:
            return Response({'error': 'Invalid key provided.'}, status=400)

        start_datetime = datetime.combine(date, time(start_hour, 0))
        end_datetime = datetime.combine(date, time(23, 59, 59))
        queryset = Project.objects.filter(
            ts__range=(start_datetime, end_datetime),
        )

        hourly_data = (
            queryset
            .annotate(hour=TruncHour('ts'))
            .values('hour')
            .annotate(
                lat=Avg('lat'),
                lon=Avg('lon'),
                humidity=Avg('humidity'),
                pressure_mb=Avg('pressure'),
                temperature_c=Avg('temperature')
            )
            .order_by('hour')
        )

        result = {"Hour":[], "Time_Block":[], "Day_of_Week": [], "temperature_c": [], "humidity": [], "pressure_mb": [], "Datetime": []}
        for entry in hourly_data:
            hour_dt = entry['hour']
            hour_int = hour_dt.hour
            result["Hour"].append(hour_int)
            result["Time_Block"].append(get_time_block(hour_int))
            result["Day_of_Week"].append(hour_dt.strftime('%A'))
            result["temperature_c"].append(entry["temperature_c"])
            result["humidity"].append(entry["humidity"])
            result["pressure_mb"].append(entry["pressure_mb"])
            result["Datetime"].append(hour_dt)
        
        df = pd.DataFrame(result)
        df = df.round({
            'temperature_c': 2,
            'humidity': 2,
            'pressure_mb': 2
        })
        column_order = ["Hour", "Time_Block", "Day_of_Week", "temperature_c", "humidity", "pressure_mb"]
        df = df[column_order]
        rating, count = model_collection.predict(key, df)
        for i in range(len(result)):
            result['Passenger_Rating'] = rating
            result['Passenger_Count'] = count
        final_result = format_json_output(result)
        return Response(final_result)
