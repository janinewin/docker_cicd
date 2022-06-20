include ../../../make.inc

.PHONY: install init_db test_dag_config test_tasks_configs test_python_functions test

init_db:
	export AIRFLOW_HOME=${PWD}; poetry run airflow db init; chmod +x tests/scripts/init_connections.sh; poetry run tests/scripts/init_connections.sh; echo 'Succesfully created db and connection'

test_dag_config:
	AIRFLOW_HOME=${PWD} poetry run pytest -v tests/test_dag_config.py

test_tasks_configs:
	AIRFLOW_HOME=${PWD} poetry run pytest -v tests/test_tasks_configs.py

test_python_functions:
	AIRFLOW_HOME=${PWD} poetry run pytest -v tests/test_python_functions.py

test:
	make init_db; AIRFLOW_HOME=${PWD} poetry run pytest -v
