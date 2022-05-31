from yaml import load
from yaml.loader import SafeLoader


def test_docker_compose():
    with open('docker-compose.yml') as f:
        docker_compose_data = load(f, SafeLoader)

    assert docker_compose_data['version'] == '3'
    postgres = docker_compose_data.get('services', {}).get('postgres', {})
    assert postgres.get('image') == 'postgres:14'
    assert postgres.get('environment') == ['POSTGRES_DB=db', 'POSTGRES_PASSWORD=$POSTGRES_PASSWORD', 'POSTGRES_USER=airflow']
    assert postgres.get('volumes') == ['./database/:/var/lib/postgresql/data']
    assert postgres.get('healthcheck', {}).get('test') == ['CMD', 'pg_isready -d db -U airflow']
    assert postgres.get('healthcheck', {}).get('interval') == '5s'
    assert postgres.get('healthcheck', {}).get('retries') == 5
    assert postgres.get('ports') == ['5432:5432']
    assert postgres.get('restart') == 'always'

    scheduler = docker_compose_data.get('services', {}).get('scheduler', {})
    assert scheduler.get('build') == '.'
    assert scheduler.get('command') == 'poetry run airflow scheduler'
    assert scheduler.get('restart') == 'on-failure'
    assert scheduler.get('depends_on') == ['postgres']
    assert scheduler.get('environment') == [
        'AIRFLOW__CORE__EXECUTOR=LocalExecutor',
        'AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:$POSTGRES_PASSWORD@postgres:5432/db'
    ]
    assert scheduler.get('volumes') == ['./dags:/opt/airflow/dags', './data:/opt/airflow/data']

    webserver = docker_compose_data.get('services', {}).get('webserver', {})
    assert webserver.get('build') == '.'
    assert webserver.get('command') in ['poetry run scripts/entrypoint.sh', 'poetry run ./scripts/entrypoint.sh']
    assert webserver.get('restart') == 'on-failure'
    assert webserver.get('depends_on') == ['postgres', 'scheduler']
    assert webserver.get('environment') == [
        'AIRFLOW__CORE__EXECUTOR=LocalExecutor',
        'AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:$POSTGRES_PASSWORD@postgres:5432/db',
        'POSTGRES_DB=db',
        'POSTGRES_PASSWORD=$POSTGRES_PASSWORD',
        'POSTGRES_USER=airflow'
    ]
    assert webserver.get('volumes') == ['./dags:/opt/airflow/dags', './data:/opt/airflow/data']
    assert webserver.get('ports') == ['8080:8080']
    assert webserver.get('healthcheck', {}).get('test') == ['CMD-SHELL', '[ -f /home/airflow/airflow-webserver.pid ]']
    assert webserver.get('healthcheck', {}).get('interval') == '30s'
    assert webserver.get('healthcheck', {}).get('timeout') == '30s'
    assert webserver.get('healthcheck', {}).get('retries') == 3
