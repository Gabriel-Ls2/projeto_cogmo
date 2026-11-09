
import os
import django
import csv

from pathlib import Path
from decimal import Decimal
from datetime import datetime
from django.db import transaction


# configura o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# importa as models
from stations.models import Station, Observation


# caminho do arquivo CSV
BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / 'observations.csv'


def importar_dados():

    # dados das estações
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

    with transaction.atomic():

        # Cadastra as estações
        for station in stations:
            Station.objects.update_or_create(
                id=station['id'],
                defaults={
                    'name': station['name'],
                    'river': station['river'],
                    'municipality': station['municipality']
                }
            )

        # Abre o arquivo CSV
        with open(CSV_PATH, 'r', newline='', encoding='utf-8') as arquivo:

            leitor = csv.DictReader(arquivo)

            for linha in leitor:

                # Busca a estação correspondente
                station = Station.objects.get(
                    id=linha['station_id']
                )

                # Converte a data para datetime
                observed_at = datetime.fromisoformat(
                    linha['observed_at'].replace('Z', '+00:00')
                )

                # Cria ou atualiza a observação
                Observation.objects.update_or_create(
                    station=station,
                    metric=linha['metric'],
                    observed_at=observed_at,
                    defaults={
                        'value': Decimal(linha['value']),
                        'unit': linha['unit'],
                        'source': linha['source']
                    }
                )

    print('Importação concluída com sucesso!')
    print(f'Estacões cadastradas: {Station.objects.count()}')
    print(f'Observações cadastradas: {Observation.objects.count()}')


if __name__ == '__main__':
    importar_dados()
