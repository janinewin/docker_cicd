FROM python:3.8.10-slim

ARG DEBIAN_FRONTEND=noninteractive

ENV PYTHONUNBUFFERED 1

ENV AIRFLOW_HOME=/opt/airflow

# DBT
ENV DBT_DIR=$AIRFLOW_HOME/lewagon_dbt
ENV DBT_TARGET_DIR=$DBT_DIR/target
ENV DBT_PROFILES_DIR=$DBT_DIR
ENV DBT_VERSION=1.1.1
RUN mkdir -p $AIRFLOW_HOME/.bigquery_keys

WORKDIR $AIRFLOW_HOME


RUN apt-get update \
    && apt-get -y upgrade \
    && apt-get -y install gnupg2 wget lsb-release\
    && sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list' \
    && wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - \
    && apt-get update \
    && apt-get -y install curl postgresql-14 postgresql-contrib \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY scripts scripts
RUN chmod +x scripts/scheduler_entrypoint.sh
RUN chmod +x scripts/webserver_entrypoint.sh

COPY pyproject.toml poetry.lock ./

RUN pip3 install --upgrade --no-cache-dir pip \
    && pip3 install poetry \
    && poetry install --no-dev
