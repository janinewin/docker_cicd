include ../../../make.inc

.PHONY: install test_docker_compose test_dockerfile test_profiles_yml init_db test_dag_config test_tasks_configs test

test_docker_compose:
	poetry run pytest -v tests/test_docker_compose.py

test_dockerfile:
	poetry run pytest -v tests/test_dockerfile.py

test_profiles_yml:
	poetry run pytest -v tests/test_profiles_yml.py

init_db:
	export AIRFLOW_HOME=${PWD}; poetry run airflow db init

test_dag_and_tasks_configs:
	AIRFLOW_HOME=${PWD} DBT_DIR=${PWD}/lewagon_dbt poetry run pytest -v tests/test_dag_and_tasks_configs.py

test:
	make init_db; AIRFLOW_HOME=${PWD} DBT_DIR=${PWD}/lewagon_dbt poetry run pytest -v

test: export AIRFLOW_HOME = ${PWD}
test: export DBT_DIR = ${PWD}/lewagon_dbt
test: init_db pytest
