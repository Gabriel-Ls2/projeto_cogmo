from .models import Station, Observation
from .serializers import StationSerializer, ObservationSerializer
from rest_framework import viewsets

class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
