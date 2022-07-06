#!/usr/bin/env bash
set -x

echo "Add connection"
airflow connections add 'sqlite_connection' \
                    --conn-type sqlite \
                    --conn-host "$PWD/airflow.db"

airflow connections add 'google_cloud_connection' \
                    --conn-type 'google_cloud_platform'
