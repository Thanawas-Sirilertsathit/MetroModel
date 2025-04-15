import os
import django
import pandas as pd
from django.utils.timezone import make_aware  

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from api.models import Project

# Load CSV
df = pd.read_csv("api_weather_historical/march_data.csv", parse_dates=["datetime"])

# Insert each row
inserted = 0
for _, row in df.iterrows():
    aware_ts = make_aware(row["datetime"])  # Convert to timezone-aware datetime

    obj, created = Project.objects.get_or_create(
        ts=aware_ts,
        defaults={
            "lat": 13.7387,  
            "lon": 100.42,
            "temperature": row["temperature_c"],
            "pressure": row["pressure_mb"],
            "humidity": row["humidity"]
        }
    )
    if created:
        inserted += 1

print(f"Done: Inserted {inserted} new rows into `project` table.")
