# API de Monitoramento Hidrológico

Projeto desenvolvido como parte do desafio COGMO, com o objetivo de construir uma API para monitoramento simulado de níveis de rios e precipitação, utilizando Python, Django REST Framework e SQLite.

A API permite consultar estações de monitoramento, visualizar as últimas medições e obter históricos de nível e chuva em determinados períodos.

> **Aviso:** Os dados utilizados neste projeto são sintéticos (simulados), não representam rios reais e não devem ser utilizados para alertas ou tomadas de decisão.

## Tecnologias utilizadas

- Python
- Django
- Django REST Framework
- SQLite
- drf-spectacular
- Swagger UI
- Redoc

## Estrutura do projeto

```text
## Estrutura do projeto

```text
projeto_cogmo/
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── docs/
│   └── diagramas do MER e DER
│
├── scripts/
│   └── seed.py
│
├── stations/
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   └── 0002_alter_observation_value.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── .gitignore
├── db.sqlite3
├── importarDados.py
├── manage.py
├── observations.csv
├── README.md
└── requirements.txt
```

## Modelagem do banco de dados

O banco de dados possui duas entidades principais:

- **Station:** armazena os dados das estações de monitoramento, incluindo nome, rio e município.
- **Observation:** armazena as observações realizadas pelas estações, incluindo métrica, data e hora, valor, unidade e origem dos dados.

Uma estação pode possuir várias observações, e cada observação pertence a uma única estação.

O banco utiliza uma restrição de unicidade para impedir registros duplicados da mesma métrica, estação e horário.

Os diagramas de modelagem estão disponíveis na pasta `docs/`.

## Requisitos

- Python instalado
- Git

## Instalação e execução

### 1. Clonar o repositório

```bash
git clone https://github.com/Gabriel-Ls2/projeto_cogmo.git
```

Acesse a pasta do projeto:

```bash
cd projeto_cogmo
```

### 2. Criar o ambiente virtual

Windows:

```bash
python -m venv venv
```

### 3. Ativar o ambiente virtual

Windows PowerShell:

```powershell
venv\Scripts\Activate
```

### 4. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 5. Executar as migrations

```bash
python manage.py migrate
```

### 6. Importar os dados

Certifique-se de que o arquivo `observations.csv` está presente na raiz do projeto.

Execute o script de importação:

```bash
python importarDados.py
```

O script cadastra as estações e importa as observações para o banco de dados SQLite.

A importação utiliza `update_or_create`, permitindo executar o script novamente sem gerar duplicações dos registros.

### 7. Iniciar o servidor

```bash
python manage.py runserver
```

O servidor estará disponível em:

[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Endpoints da API

### Listar estações

**GET** `/api/stations/`

Retorna todas as estações cadastradas.

### Consultar estação

**GET** `/api/stations/{id}/`

Retorna os dados de uma estação específica.

### Consultar resumo da estação

**GET** `/api/stations/{id}/summary/`

Retorna os dados da estação e suas últimas observações de nível e chuva.

Exemplo:

```http
GET /api/stations/EST-01/summary/
```

### Consultar histórico de medições

**GET** `/api/stations/{id}/series/`

Retorna o histórico de medições de uma estação, de acordo com a métrica e o período informados.

Parâmetros:

| Parâmetro | Tipo    | Obrigatório | Descrição                                  |
| --------- | ------- | ----------- | ------------------------------------------ |
| metric    | string  | Sim         | Métrica consultada: `level` ou `rain`      |
| hours     | integer | Não         | Período em horas, entre 1 e 72. Padrão: 24 |

Exemplo:

```http
GET /api/stations/EST-01/series/?metric=level&hours=24
```

Consultar precipitação:

```http
GET /api/stations/EST-01/series/?metric=rain&hours=24
```

As observações são retornadas em ordem cronológica.

## Documentação da API

A documentação interativa está disponível através do Swagger UI:

[http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/)

A documentação alternativa está disponível através do Redoc:

[http://127.0.0.1:8000/api/redoc/](http://127.0.0.1:8000/api/redoc/)

## Estações cadastradas

| ID     | Estação            | Rio          | Município   |
| ------ | ------------------ | ------------ | ----------- |
| EST-01 | Estação Aurora     | Rio Aurora   | Vila Aurora |
| EST-02 | Estação Vale Verde | Rio Verde    | Vale Verde  |
| EST-03 | Estação Campo Alto | Rio do Campo | Campo Alto  |

## Métricas disponíveis

| Métrica | Descrição    | Unidade |
| ------- | ------------ | ------- |
| `level` | Nível do rio | m       |
| `rain`  | Precipitação | mm/h    |

## Tratamento de erros

A API realiza validações dos parâmetros informados nas requisições.

| Código HTTP | Descrição                        |
| ----------- | -------------------------------- |
| 200         | Requisição realizada com sucesso |
| 400         | Parâmetros inválidos             |
| 404         | Estação não encontrada           |

## Autor

Projeto desenvolvido durante a Residência Tecnológica em Desenvolvimento de Software – Bolsa Futuro Digital.
