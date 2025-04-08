import pandas as pd

RATING_MAP = {"Very Low": 0, "Low": 1, "Moderate": 2, "Crowded": 3, "Dense": 4, "Very Dense": 5}
EXAMPLE_DATA = pd.DataFrame({
    "Hour": [9, 13, 17],    
    "Time_Block": ["Morning", "Afternoon", "Evening"],
    "Day_of_Week": ["Saturday", "Friday", "Sunday"],
    "temperature_c": [30.2, 36.5, 37.5],
    "humidity": [70, 82, 50],
    "pressure_mb": [1005.1, 1003.7, 1100.2],
})
