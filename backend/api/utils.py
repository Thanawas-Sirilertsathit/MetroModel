def get_time_block(hour):
    """Return time block."""
    if 5 <= hour < 12:
        return 'Morning'
    elif 12 <= hour < 16:
        return 'Afternoon'
    elif 16 <= hour < 21:
        return 'Evening'
    else:
        return 'Night'

def format_json_output(dictionary):
    """Format hourly data into list of JSON dicts."""
    output = []
    for i in range(len(dictionary["Hour"])):
        output.append({
            "Hour": dictionary["Hour"][i],
            "Time_Block": dictionary["Time_Block"][i],
            "Day_of_Week": dictionary["Day_of_Week"][i],
            "temperature_c": dictionary["temperature_c"][i],
            "humidity": dictionary["humidity"][i],
            "pressure_mb": dictionary["pressure_mb"][i],
            "Datetime": dictionary["Datetime"][i],
            "Passenger_Rating": dictionary["Passenger_Rating"][i],
            "Passenger_Count": dictionary["Passenger_Count"][i],
        })
    return output
