#!/usr/bin/env bash

export PGPASSWORD="$POSTGRES_PASSWORD"
until psql -h "postgres" -d "$POSTGRES_DB" -U "$POSTGRES_USER" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"

airflow db upgrade

airflow users create -r Admin -u admin -p admin -e admin@example.com -f admin -l airflow

scripts/init_connections.sh

airflow webserver
