#!/usr/bin/env bash

python scripts/create_airflow_service_account_json.py

poetry run airflow scheduler
