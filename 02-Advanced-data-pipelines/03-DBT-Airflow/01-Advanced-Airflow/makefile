.PHONY: install init_db test_dag_config test_tasks_configs test_python_functions test

install:
	poetry install

init_db:
	export AIRFLOW_HOME=${PWD}; poetry run airflow db init; chmod +x tests/init_connections.sh; poetry run tests/init_connections.sh; echo 'Succesfully created db and connection'

test_extract_dag:
	AIRFLOW_HOME=${PWD} poetry run pytest -v tests/test_extract_dag.py

test_transform_dag:
	AIRFLOW_HOME=${PWD} poetry run pytest -v tests/test_transform_dag.py

test_load_dag:
	AIRFLOW_HOME=${PWD} poetry run pytest -v tests/test_load_dag.py

test:
	export AIRFLOW_HOME=${PWD}; make init_db; poetry run pytest -v
