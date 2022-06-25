.PHONY: install init_db test_dag_config test_python_functions test_tasks_configs test

install:
	poetry install

init_db:
	export AIRFLOW_HOME=${PWD}; poetry run airflow db init

test_dag_config:
	DBT_DIR=${PWD}/tests/dbt AIRFLOW_HOME=${PWD} poetry run pytest -v tests/test_dag_config.py

test_python_functions:
	DBT_DIR=${PWD}/tests/dbt AIRFLOW_HOME=${PWD} poetry run pytest -v tests/test_python_functions.py

test_tasks_configs:
	DBT_DIR=${PWD}/tests/dbt AIRFLOW_HOME=${PWD} poetry run pytest -v tests/test_tasks_configs.py

test:
	make init_db; DBT_DIR=${PWD}/tests/dbt AIRFLOW_HOME=${PWD} poetry run pytest -v
