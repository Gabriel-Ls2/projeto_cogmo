from .models import Station, Observation
from .serializers import StationSerializer, ObservationSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

class StationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer


    @action(detail=True, methods=['get'])
    def summary(self, request, pk=None):

        station = self.get_object()

        latest_level = station.observations.filter(metric='level').order_by('-observed_at').first()

        latest_rain = station.observations.filter(metric='rain').order_by('-observed_at').first()

        return Response({
            'station': StationSerializer(station).data,

            'latest_level': {
                'value': latest_level.value,
                'unit': latest_level.unit,
                'observed_at': latest_level.observed_at
            } if latest_level else None,

            'latest_rain': {
                'value': latest_rain.value,
                'unit': latest_rain.unit,
                'observed_at': latest_rain.observed_at
            } if latest_rain else None
        })

