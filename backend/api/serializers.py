from rest_framework import serializers

class HourlyDataSerializer(serializers.Serializer):
    Hour = serializers.IntegerField()
    Time_Block = serializers.CharField()
    Day_of_Week = serializers.CharField()
    temperature_c = serializers.FloatField()
    humidity = serializers.FloatField()
    pressure_mb = serializers.FloatField()

class OneDayResultSerializer(serializers.Serializer):
    Passenger_Rating = serializers.CharField()
    Passenger_Count = serializers.IntegerField()
    Data = HourlyDataSerializer(many=True)

class ShortHourlySerializer(serializers.Serializer):
    hour = serializers.DateTimeField()
    lat = serializers.FloatField()
    lon = serializers.FloatField()
    humid = serializers.FloatField()
    pressure = serializers.FloatField()
    temp = serializers.FloatField()

class PredictionInputSerializer(serializers.Serializer):
    temperature_c = serializers.FloatField()
    humidity = serializers.FloatField()
    pressure_mb = serializers.FloatField()
    day_of_week = serializers.CharField()
    time = serializers.TimeField(format="%H:%M", input_formats=["%H:%M"])
    key = serializers.IntegerField()

class PredictionOutputSerializer(serializers.Serializer):
    Passenger_Rating = serializers.CharField()
    Passenger_Count = serializers.IntegerField()
