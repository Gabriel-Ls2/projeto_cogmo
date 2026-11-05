
import csv
import math
from datetime import datetime, timedelta, timezone
from pathlib import Path

# estações fictícias
stations = [
    {
        'id': 'EST-01',
        'name': 'Estação Aurora',
        'river': 'Rio Aurora',
        'municipality': 'Vila Aurora'
    },
    {
        'id': 'EST-02',
        'name': 'Estação Vale Verde',
        'river': 'Rio Verde',
        'municipality': 'Vale Verde'
    },
    {
        'id': 'EST-03',
        'name': 'Estação Campo Alto',
        'river': 'Rio do Campo',
        'municipality': 'Campo Alto'
    }
]


# arredonda o horário atual para a hora cheia em UTC
now = datetime.now(timezone.utc)

end_hour = now.replace(
    minute=0,
    second=0,
    microsecond=0
)

observations = []


# gera 73 horários para cada estação
for index in range(73):

    timestamp = end_hour - timedelta(hours=(72 - index))

    observed_at = timestamp.isoformat(
        timespec='seconds'
    ).replace('+00:00', 'Z')

    for station_index, station in enumerate(stations):

        # gera o nível do rio
        level = (
            1.05
            + station_index * 0.24
            + 0.08 * math.sin(index / 5 + station_index)
        )

        # gera a quantidade de chuva
        if (index + station_index * 7) % 17 < 3:
            rain = (
                0.4
                + ((index + station_index) % 4) * 0.35
            )
        else:
            rain = 0

        # registra o nível
        observations.append({
            'station_id': station['id'],
            'metric': 'level',
            'observed_at': observed_at,
            'value': round(level, 2),
            'unit': 'm',
            'source': 'synthetic'
        })

        # registra a chuva
        observations.append({
            'station_id': station['id'],
            'metric': 'rain',
            'observed_at': observed_at,
            'value': round(rain, 2),
            'unit': 'mm/h',
            'source': 'synthetic'
        })


# caminho do arquivo CSV na raiz do projeto
output_path = Path(__file__).resolve().parent.parent / 'observations.csv'

# exporta as observações
with open(output_path, 'w', newline='', encoding='utf-8') as file:

    fieldnames = [
        'station_id',
        'metric',
        'observed_at',
        'value',
        'unit',
        'source'
    ]

    writer = csv.DictWriter(
        file,
        fieldnames=fieldnames
    )

    writer.writeheader()
    writer.writerows(observations)


print(f'Arquivo gerado: {output_path}')
print(f'Total de observações: {len(observations)}')
