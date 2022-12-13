.PHONY: test_docker_compose test_dockerfile test_profiles_yml test_dag_config test_tasks_configs test

# Our tests will re-create a SQLite copy of your postgres db inside the "temp" folder, and then test against this sqlite db
AIRFLOW_HOME=${PWD}/tests/temp
DBT_DIR=${PWD}/dbt_lewagon

test_docker_compose:
	pytest -v --disable-warnings tests/test_docker_compose.py

test_dockerfile:
	pytest -v --disable-warnings tests/test_dockerfile.py

test_profiles_yml:
	pytest -v --disable-warnings tests/test_profiles_yml.py

test_dag_and_tasks_configs:
	export AIRFLOW_HOME=${AIRFLOW_HOME}; \
	export DBT_DIR=${DBT_DIR}; \
	airflow db init; \
	pytest -v --disable-warnings tests/test_dag_and_tasks_configs.py

test:
	export AIRFLOW_HOME=${AIRFLOW_HOME}; \
	export DBT_DIR=${DBT_DIR}; \
	airflow db init; \
	pytest tests -m "not optional" -v --disable-warnings 2>&1 > test_output.txt || echo "-- Some tests didn't pass, let's look at the output"; \
	pytest tests -m "not optional" -v --disable-warnings --color=yes
