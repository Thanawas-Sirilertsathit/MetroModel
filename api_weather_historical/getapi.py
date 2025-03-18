import requests
import time
import csv
from datetime import datetime, timedelta

API_KEY = 'Your api key'
LOCATION = 'Bangkok'
START_DATE = datetime(2021, 1, 24)
END_DATE = datetime(2021, 1, 24)

url = 'https://api.weatherapi.com/v1/history.json'
csv_file = 'weather_hourly_data.csv'

# Write header
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['datetime', 'temperature_c', 'humidity', 'pressure_mb'])

# Loop through each day
current_date = START_DATE

while current_date <= END_DATE:
    formatted_date = current_date.strftime('%Y-%m-%d')
    params = {
        'key': API_KEY,
        'q': LOCATION,
        'dt': formatted_date
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        hourly_data = data['forecast']['forecastday'][0]['hour']
        with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for hour in hourly_data:
                writer.writerow([
                    hour['time'],
                    hour['temp_c'],
                    hour['humidity'],
                    hour['pressure_mb']
                ])
        print(f"Saved hourly data for {formatted_date}")
    except Exception as e:
        print(f"Error on {formatted_date}: {e}")
    current_date += timedelta(days=1)
    time.sleep(5)
