from rest_framework import serializers
from .models import Station, Observation

class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = '__all__'

class ObservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Observation
        fields = '__all__'  

# serializers especificos para os endpoints summary e series, por conta da documentação 

class LatestReadingSerializer(serializers.Serializer):
    value = serializers.CharField()
    unit = serializers.CharField()
    source = serializers.CharField()
    observed_at = serializers.DateTimeField()


class SummarySerializer(serializers.Serializer):
    station = StationSerializer()
    latest_level = LatestReadingSerializer(allow_null=True)
    latest_rain = LatestReadingSerializer(allow_null=True)


class SeriesResponseSerializer(serializers.Serializer):
    observations = ObservationSerializer(many=True)