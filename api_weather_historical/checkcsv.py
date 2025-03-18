import csv
from datetime import datetime, timedelta

start_date = datetime(2021, 1, 1)
end_date = datetime(2025, 2, 28)
csv_file = 'weather_hourly_data.csv'
dates_in_csv = set()

with open(csv_file, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        dt = row['datetime']
        try:
            date_only = dt.split(' ')[0]
            dates_in_csv.add(date_only)
        except Exception as e:
            print(f"Error parsing row: {row} – {e}")

missing_dates = []
current = start_date

while current <= end_date:
    date_str = current.strftime('%Y-%m-%d')
    if date_str not in dates_in_csv:
        missing_dates.append(date_str)
    current += timedelta(days=1)

if missing_dates:
    print("❌ Missing Dates:")
    for d in missing_dates:
        print(d)
else:
    print("✅ All dates present from 2021-01-01 to 2025-02-28.")
