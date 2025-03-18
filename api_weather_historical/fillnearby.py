import csv
from datetime import datetime
from collections import defaultdict

csv_file = 'weather_hourly_data.csv'

all_rows = []
with open(csv_file, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        all_rows.append(row)

daily_data = defaultdict(list)
for row in all_rows:
    date = row['datetime'].split(' ')[0]
    daily_data[date].append(row)

day_before = '2021-01-23'
day_after = '2021-01-25'
# We had a missing value for a day 2021-01-24
target_day = '2021-01-24'

if target_day not in daily_data and day_before in daily_data and day_after in daily_data:
    rows_23 = sorted(daily_data[day_before], key=lambda x: x['datetime'])
    rows_25 = sorted(daily_data[day_after], key=lambda x: x['datetime'])
    new_rows = []
    for i in range(24):
        hour = f"{i:02d}:00"
        dt = f"{target_day} {hour}"
        temp = (float(rows_23[i]['temperature_c']) + float(rows_25[i]['temperature_c'])) / 2
        humidity = (float(rows_23[i]['humidity']) + float(rows_25[i]['humidity'])) / 2
        pressure = (float(rows_23[i]['pressure_mb']) + float(rows_25[i]['pressure_mb'])) / 2
        new_rows.append({
            'datetime': dt,
            'temperature_c': round(temp, 1),
            'humidity': int(round(humidity)),
            'pressure_mb': round(pressure, 1)
        })
    all_rows.extend(new_rows)
    print(f"✅ Filled missing data for {target_day}")
else:
    print(f"⚠️ Skipped filling {target_day}: Already exists or missing neighbors.")

all_rows = sorted(all_rows, key=lambda x: datetime.strptime(x['datetime'], '%Y-%m-%d %H:%M'))
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    fieldnames = ['datetime', 'temperature_c', 'humidity', 'pressure_mb']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_rows)

print(f"✅ CSV updated and sorted.")
