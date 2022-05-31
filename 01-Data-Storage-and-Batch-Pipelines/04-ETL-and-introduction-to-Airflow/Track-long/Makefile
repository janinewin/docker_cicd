.PHONY: install init_db test_connection test_dag_config test_tasks_configs test_python_functions test

install:
	poetry install

init_db:
	export AIRFLOW_HOME=${PWD}; poetry run airflow db init; chmod +x tests/init_connections.sh; poetry run tests/init_connections.sh; echo 'Succesfully created db and connection'

test_dag_config:
	poetry run pytest -v tests/test_dag_config.py

test_tasks_configs:
	AIRFLOW_HOME=${PWD} poetry run pytest -v tests/test_tasks_configs.py

test_python_functions:
	poetry run pytest -v tests/test_python_functions.py

test:
	make init_db; AIRFLOW_HOME=${PWD} poetry run pytest -v
