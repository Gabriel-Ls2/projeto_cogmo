from .models import Station
from .serializers import StationSerializer, ObservationSerializer
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import timedelta

class StationViewSet(viewsets.ReadOnlyModelViewSet):
    # endpoint de listagem de estações
    queryset = Station.objects.all()
    serializer_class = StationSerializer

    # endpoint summary para uma estação específica, retornando a última observação de nível e chuva
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

    # endpoint series para uma estação específica, retornando as observações de nível ou chuva em um período de horas
    @action(detail=True, methods=['get'])
    def series(self, request, pk=None):
        station = self.get_object()

        # recebe os parâmetros da requisição
        metric = request.query_params.get('metric')
        hours = request.query_params.get('hours', 24)

        if metric not in ['level', 'rain']:
            return Response({'detail': 'Métrica inválida. Use level ou rain.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            hours = int(hours)
        except (ValueError, TypeError):
            return Response({'detail': 'hours deve ser um número inteiro.'}, status=status.HTTP_400_BAD_REQUEST)

        if hours < 1 or hours > 72:
            return Response({'detail': 'hours deve estar entre 1 e 72.'}, status=status.HTTP_400_BAD_REQUEST)

        latest_observation = station.observations.filter(metric=metric).order_by('-observed_at').first()

        if not latest_observation:
            return Response([])

        # calcula o início da janela temporal
        start_time = latest_observation.observed_at - timedelta(hours=hours)

        # filtra as observações do período
        observations = station.observations.filter(metric=metric, observed_at__gte=start_time, observed_at__lte=latest_observation.observed_at).order_by('observed_at')

        serializer = ObservationSerializer(observations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)