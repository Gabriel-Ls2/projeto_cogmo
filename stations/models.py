from django.db import models

class Station(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=100)
    river = models.CharField(max_length=100)
    municipality = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Observation(models.Model):
    METRIC_CHOICES = [
        ('level', 'Nível do rio'),
        ('rain', 'Chuva'),
    ]

    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='observations')
    metric = models.CharField(max_length=10, choices=METRIC_CHOICES)
    observed_at = models.DateTimeField()
    value = models.DecimalField(max_digits=8, decimal_places=2)
    unit = models.CharField(max_length=10)
    source = models.CharField(max_length=20, default='synthetic')

    class Meta:
        constraints = [
            # garante idempotência: impede duplicidade da mesma métrica no mesmo horário na mesma estação
            models.UniqueConstraint(
                fields=['station', 'metric', 'observed_at'],
                name='unique_station_metric_timestamp'
            )
        ]

    def __str__(self):
        return f'{self.station.name} - {self.metric}'