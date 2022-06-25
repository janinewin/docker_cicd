from yaml import load
from yaml.loader import SafeLoader


def test_docker_compose():
    with open("docker-compose.yml") as f:
        docker_compose_data = load(f, SafeLoader)

    assert docker_compose_data["version"] == "3"
    postgres = docker_compose_data.get("services", {}).get("postgres", {})
    assert postgres.get("image") == "postgres:14"
    assert set(postgres.get("environment")) == set(
        [
            "POSTGRES_DB=db",
            "POSTGRES_PASSWORD=$POSTGRES_PASSWORD",
            "POSTGRES_USER=airflow",
        ]
    )
    assert postgres.get("volumes") == ["./database/:/var/lib/postgresql/data"]
    assert postgres.get("healthcheck", {}).get("test") == [
        "CMD",
        "pg_isready -d db -U airflow",
    ]
    assert postgres.get("healthcheck", {}).get("interval") == "5s"
    assert postgres.get("healthcheck", {}).get("retries") == 5
    assert postgres.get("ports") == ["5432:5432"]
    assert postgres.get("restart") == "always"

    scheduler = docker_compose_data.get("services", {}).get("scheduler", {})
    assert scheduler.get("build") == "."
    assert scheduler.get("command") in [
        "poetry run scripts/scheduler_entrypoint.sh",
        "poetry run ./scripts/scheduler_entrypoint.sh",
    ]
    assert scheduler.get("restart") == "on-failure"
    assert scheduler.get("depends_on") == ["postgres"]
    assert set(scheduler.get("environment")) == set(
        [
            "AIRFLOW__CORE__EXECUTOR=LocalExecutor",
            "AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:$POSTGRES_PASSWORD@postgres:5432/db",
            "AIRFLOW__CORE__LOAD_EXAMPLES=false",
            "PROJECT_ID=$PROJECT_ID",
            "PRIVATE_KEY_ID=$PRIVATE_KEY_ID",
            "PRIVATE_KEY=$PRIVATE_KEY",
            "CLIENT_EMAIL=$CLIENT_EMAIL",
            "CLIENT_ID=$CLIENT_ID",
            "CLIENT_X509_CERT_URL=$CLIENT_X509_CERT_URL",
        ]
    )
    assert set(scheduler.get("volumes")) == set(
        [
            "./dags:/opt/airflow/dags",
            "./data:/opt/airflow/data",
            "./logs:/opt/airflow/logs",
            "./lewagon_dbt:/opt/airflow/lewagon_dbt",
        ]
    )

    webserver = docker_compose_data.get("services", {}).get("webserver", {})
    assert webserver.get("build") == "."
    assert webserver.get("command") in [
        "poetry run scripts/webserver_entrypoint.sh",
        "poetry run ./scripts/webserver_entrypoint.sh",
    ]
    assert webserver.get("restart") == "on-failure"
    assert set(webserver.get("depends_on")) == set(["postgres", "scheduler"])
    assert set(webserver.get("environment")) == set(
        [
            "AIRFLOW__CORE__EXECUTOR=LocalExecutor",
            "AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:$POSTGRES_PASSWORD@postgres:5432/db",
            "POSTGRES_DB=db",
            "POSTGRES_PASSWORD=$POSTGRES_PASSWORD",
            "POSTGRES_USER=airflow",
        ]
    )
    assert set(webserver.get("volumes")) == set(
        [
            "./dags:/opt/airflow/dags",
            "./data:/opt/airflow/data",
            "./logs:/opt/airflow/logs",
            "./lewagon_dbt:/opt/airflow/lewagon_dbt",
        ]
    )
    assert webserver.get("ports") == ["8080:8080"]
    assert webserver.get("healthcheck", {}).get("test") == [
        "CMD-SHELL",
        "[ -f /home/airflow/airflow-webserver.pid ]",
    ]
    assert webserver.get("healthcheck", {}).get("interval") == "30s"
    assert webserver.get("healthcheck", {}).get("timeout") == "30s"
    assert webserver.get("healthcheck", {}).get("retries") == 3
