import re

import dockerfile
import pytest


@pytest.fixture
def dockerfile_validation():
    return [
        ("FROM", "python:3.8.12-slim"),
        ("ARG", "DEBIAN_FRONTEND=noninteractive"),
        ("ENV", "PYTHONUNBUFFERED 1"),
        ("ENV", "AIRFLOW_HOME /opt/airflow"),
        ("WORKDIR", "$AIRFLOW_HOME"),
        (
            "RUN",
            "apt-get update && apt-get -y upgrade && apt-get -y install gnupg2 wget lsb-release && sh -c 'echo \"deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main\" > /etc/apt/sources.list.d/pgdg.list' && wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - && apt-get update && apt-get -y install curl postgresql-14 postgresql-contrib && apt-get clean && rm -rf /var/lib/apt/lists/*",
        ),  # noqa
        ("COPY", "scripts scripts"),
        ("RUN", "chmod +x scripts/entrypoint.sh"),
        ("COPY", "pyproject.toml poetry.lock ./"),
        ("RUN", "pip3 install --upgrade --no-cache-dir pip && pip3 install poetry && poetry install --no-dev"),
    ]


def test_dockerfile(dockerfile_validation):
    dockerfile_name = "Dockerfile"
    dockerfile_parsed = dockerfile.parse_file(dockerfile_name)

    assert len(dockerfile_parsed) == len(dockerfile_validation)

    for command, validation in zip(dockerfile_parsed, dockerfile_validation):
        assert command.cmd == validation[0]
        if command.cmd == "RUN":
            s = re.sub(r"\s+", " ", command.value[0])
            assert s == validation[1]
        elif len(command.flags) != 0:
            assert " ".join([" ".join(command.flags), " ".join(command.value)]) == validation[1]
        else:
            assert " ".join(command.value) == validation[1]
