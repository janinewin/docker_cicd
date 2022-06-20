import pytest
from yaml import dump, load
from yaml.loader import SafeLoader


class TestTask3:
    @pytest.fixture
    def docker_validation(self):
        return load(
            """
            version: '3.9'
            services:
                webapi:
                    container_name: fastapi
                    build:
                        context: .
                        dockerfile: dockerfile-fastapi
                    restart: on-failure
                    ports:
                        - "8000:8000"
                    volumes:
                        - ./app:/server/app
                    command: ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
                    networks:
                        - backend
                    depends_on:
                        - database

                database:
                    image: postgres:14.2
                    restart: on-failure  
                    healthcheck:
                        test: ["CMD", "pg_isready -U postgres"]
                        interval: 5s
                        timeout: 5s
                        retries: 5
                    volumes:
                        - ./database/:/docker-entrypoint-initdb.d/
                    environment:
                        - POSTGRES_USER=postgres
                        - POSTGRES_PASSWORD=postgres
                        - APP_DB_USER=goldenspice
                        - APP_DB_PASS=whatsupdawg
                        - APP_DB_NAME=gangstadb
                    ports:
                        - 5432:5432
                    networks:
                        - backend

            networks:
                backend:
                    driver: bridge
            """,
            SafeLoader,
        )

    def test_docker_compose(self, docker_validation):
        keys_to_check = ["webapi", "container_name", "restart", "ports", "networks", "environment", "volumes"]

        def get_keys(d, keys=None):
            keys = keys or []
            if isinstance(d, dict):
                keys += d.keys()
                _ = [get_keys(x, keys) for x in d.values()]
            elif isinstance(d, list):
                _ = [get_keys(x, keys) for x in d]
            return list(set(keys))

        with open("docker-compose-3.yml") as f:
            docker_compose_data = load(f, SafeLoader)

            keys = get_keys(docker_compose_data)
            assert all(item in keys for item in keys_to_check)
