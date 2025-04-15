from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Avg
from django.db.models.functions import TruncHour
from .models import Project
import pandas as pd

class MergedWeatherAPIView(APIView):
    def get(self, request):
        # DB data
        db_qs = (
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
        )
        db_df = pd.DataFrame(db_qs)

        # CSV data (March)
        try:
            csv_df = pd.read_csv('api_weather_historical/march_data.csv', parse_dates=['datetime'])
            csv_df['hour'] = csv_df['datetime'].dt.floor('H')
            csv_df_grouped = csv_df.groupby('hour').agg({
                'temperature_c': 'mean',
                'humidity': 'mean',
                'pressure_mb': 'mean'
            }).reset_index()
            csv_df_grouped.rename(columns={
                'temperature_c': 'temp',
                'humidity': 'humid',
                'pressure_mb': 'pressure'
            }, inplace=True)
            csv_df_grouped['lat'] = 13.7563
            csv_df_grouped['lon'] = 100.5018
        except Exception as e:
            print(f"CSV error: {e}")
            csv_df_grouped = pd.DataFrame(columns=['hour', 'temp', 'humid', 'pressure', 'lat', 'lon'])

        # Merge and sort
        combined_df = pd.concat([db_df, csv_df_grouped], ignore_index=True)
        combined_df = combined_df.sort_values(by='hour')

        return Response(combined_df.to_dict(orient='records'))
