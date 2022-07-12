include ../../../make.inc

.PHONY: install init_db test_extract_dag test_transform_dag test_load_dag test

init_db:
	export AIRFLOW_HOME=${PWD}; poetry run airflow db init; chmod +x tests/scripts/init_connections.sh; poetry run tests/scripts/init_connections.sh; echo 'Succesfully created db and connection'

test_extract_dag:
	AIRFLOW_HOME=${PWD} poetry run pytest -v tests/test_extract_dag.py

test_transform_dag:
	AIRFLOW_HOME=${PWD} poetry run pytest -v tests/test_transform_dag.py

test_load_dag:
	AIRFLOW_HOME=${PWD} poetry run pytest -v tests/test_load_dag.py

test: export AIRFLOW_HOME = ${PWD}
test: init_db pytest
