import pandas as pd
from django.db.models import Avg
from django.db.models.functions import TruncHour
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Project
from datetime import datetime, time
from .model_registry import model_collection
from .utils import get_time_block, format_json_output
from .serializers import OneDayResultSerializer, ShortHourlySerializer, PredictionInputSerializer, PredictionOutputSerializer
from drf_spectacular.utils import extend_schema

class ProjectHourlyAverageAPIView(APIView):
    """API for getting all data in the database but without prediction"""
    @extend_schema(
        responses=ShortHourlySerializer(many=True),
        description="Returns all hourly-aggregated records in the database without prediction."
    )
    def get(self, request, *args, **kwargs):
        """Get request for retrieving all data in the database without prediction."""
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
    """API for getting data with one day range."""
    START_EARLY = [1, 2, 3, 4, 8]
    START_LATE = [5, 6, 7]
    @extend_schema(
        responses=OneDayResultSerializer,
        description="Returns averaged hourly data for the day, including predicted passenger rating and count. Requires query parameters (key and date)."
    )
    def get(self, request, *args, **kwargs):
        """Get the data with the predicted result using query parameter (key and date)."""
        params = self.validate_and_parse_params(request)
        if isinstance(params, Response):
            return params
        date, key = params
        start_datetime, end_datetime = self.get_time_range(date, key)
        if isinstance(start_datetime, Response):
            return start_datetime
        hourly_data = self.get_hourly_data(start_datetime, end_datetime)
        df, result = self.process_hourly_data(hourly_data)
        rating, count = model_collection.predict(key, df)
        result['Passenger_Rating'] = rating
        result['Passenger_Count'] = count
        final_result = format_json_output(result)
        return Response(final_result)

    def validate_and_parse_params(self, request):
        """Extract query parameters."""
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
        return date, key

    def get_time_range(self, date, key):
        """Get time range for each organization."""
        if key in self.START_EARLY:
            start_hour = 5
        elif key in self.START_LATE:
            start_hour = 6
        else:
            return Response({'error': 'Invalid key provided.'}, status=400)
        start_datetime = datetime.combine(date, time(start_hour, 0))
        end_datetime = datetime.combine(date, time(23, 59, 59))
        return start_datetime, end_datetime

    def get_hourly_data(self, start_datetime, end_datetime):
        """Get data from database with start time and end time."""
        queryset = Project.objects.filter(ts__range=(start_datetime, end_datetime))
        return (
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

    def process_hourly_data(self, hourly_data):
        """Create more columns in dataframe before going to use it to predict values."""
        result = {
            "Hour": [],
            "Time_Block": [],
            "Day_of_Week": [],
            "temperature_c": [],
            "humidity": [],
            "pressure_mb": [],
            "Datetime": []
        }
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
        return df, result

class ProjectPredictionAPIView(APIView):
    """POST API for predicting values based on input features."""
    @extend_schema(
        request=PredictionInputSerializer,
        responses=PredictionOutputSerializer,
        description="Predicts passenger rating and count from weather, key and time inputs. All required data: temperature_c, humidity, pressure_mb, day_of_week, time and key."
    )
    def post(self, request, *args, **kwargs):
        """Post request for predicting values with inputs (temperature_c, humidity, pressure_mb, day_of_week, time and key)."""
        data = request.data
        required_fields = ["temperature_c", "humidity", "pressure_mb", "day_of_week", "time", "key"]
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return Response(
                {"error": f"Missing fields: {', '.join(missing_fields)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            temperature = float(data["temperature_c"])
            humidity = float(data["humidity"])
            pressure = float(data["pressure_mb"])
            day_of_week = data["day_of_week"]
            time_obj = datetime.strptime(data["time"], "%H:%M").time()
            hour = time_obj.hour
            time_block = get_time_block(hour)
            key = int(data["key"])
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        input_dict = {
            "Hour": [hour],
            "Time_Block": [time_block],
            "Day_of_Week": [day_of_week],
            "temperature_c": [temperature],
            "humidity": [humidity],
            "pressure_mb": [pressure]
        }
        df = pd.DataFrame(input_dict)
        try:
            rating, count = model_collection.predict(key, df)
        except Exception as e:
            return Response({"error": f"Prediction failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            "Passenger_Rating": rating,
            "Passenger_Count": count
        })
