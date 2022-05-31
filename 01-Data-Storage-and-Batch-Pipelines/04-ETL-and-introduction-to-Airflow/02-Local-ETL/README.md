# Local ETL

### Introduction

In this challenge, you will create a local E(xtract)T(ransform)L(oad).

The goal is to have a DAG running every day that will:
- downloads a Chuck Norris' joke (Extract)
- translates it to Swedish (Transform)
- inserts it into our Postgres database (Load)

For the Chuck Norris' joke, you will use this api: https://api.chucknorris.io

You will save the jokes and their translated versions to JSON before inserting them to your PostgreSQL database that will play the roles of "Datalake" (your JSON files) and "Datawarehouse" (your PostgreSQL database). Of course, in production you would use other tools than JSON and PostgreSQL that are not real Datalake and Datawarehouse. In addition, you would not use the same Database for two different purposes (storing Airflow metadata + storing data for our ETL) but let's keep it simple for now.

As for the previous exercise, we split the instructions in four parts to help you create the this local ETL.

### Setup Instructions

As explained above, you will have to interact with your PostgreSQL database from your DAG. To do so, you will use the [PostgresHook class](https://airflow.apache.org/docs/apache-airflow-providers-postgres/stable/_api/airflow/providers/postgres/hooks/postgres/index.html#module-airflow.providers.postgres.hooks.postgres). As you can see by reading the documentation, when instantiating a PostgresHook, you have to pass a `connection_id` corresponding to the database that you want to connect to. The first step to be able to use a `PostgresHook` in your DAG is thus to create a connection to your database.

To create this connection, you will have to create a file named `scripts/init_connections.sh` (note that we have slightly updated the Dockerfile & docker-compose to run this file). Then copy paste the following lines in your `scripts/init_connections.sh`:

```
#!/usr/bin/env bash
set -x

echo "Add connection"
airflow connections add 'postgres_connection' \
                    --conn-type postgres \
                    --conn-host "postgres" \
                    --conn-schema "$POSTGRES_DB" \
                    --conn-login "$POSTGRES_USER" \
                    --conn-password "$POSTGRES_PASSWORD" \
                    --conn-port "5432"
```

As you can see, we use the Airflow command line interface to create a connection named `postgres_connection` that stores our database connection's configurations.

Apart from that, the dockerfile and the docker-compose are the same as the ones you created in the setup exercise, and we have already prepared the pyproject.toml for you.

Make sure your terminal is in the current exercise folder and let's start by creating a local Airflow database for pytest by running:

```
make init_db
```

It should create the three same files as for the previous exercise, and an Airflow connection to this database (that will be used in the tests only). If you inspect the test files, you could see that we use an sqlite database to test your functions and not a PostgreSQL as you use for your Airflow instance. We do that, because a sqlite database is much lighter and is stored in a simple file, which makes the tests easier to setup.

As before, Create an `.env` file and set `POSTGRES_PASSWORD` to the value of your choice.

Take time to open the `dags/local_etl.py` and discover the functions signatures that we have added to help you.

## DAG Instructions

First, let's focus on creating the proper DAG configuration (no tasks or python functions needed for now).

You need to create a dag with the following requirements:
- it should be named `local_etl`
- it should have a start date equal to five days ago
- it should have a description saying `A local etl`
- it should catchup the missing runs
- it should be scheduled to run every day
- it should run only if the previous runs succeed

Once, you are confident with your code run:
```
make test_dag_config
```

## Tasks Instructions

Then, we want you to create the tasks that your DAG will use.

You need four tasks:

- A [PostgresOperator](https://airflow.apache.org/docs/apache-airflow-providers-postgres/stable/_api/airflow/providers/postgres/operators/postgres/index.html#module-airflow.providers.postgres.operators.postgres) with a `task_id` named `create_swedified_jokes_table` that should create a table named swedified_jokes with three columns (`id`, `joke` and `swedified_joke` that should be a `primary key` and two not null `varchar` columns).


- A [BashOperator](https://airflow.apache.org/docs/apache-airflow/stable/howto/operator/bash.html) to [curl]((https://en.wikipedia.org/wiki/CURL) a random Chuck Norris' joke from https://api.chucknorris.io with a `task_id` named `extract`. The joke should be saved to the bronze folder under the name joke_<execution_date>.json where <execution_date> corresponds to the execution date of the Airflow dag (for instance: data/bronze/joke_20220521.json). Have a look to Airflow templates reference for that: https://airflow.apache.org/docs/apache-airflow/stable/templates-ref.html

- A `PythonOperator` with a `task_id` named `transform` that should trigger the `transform` function with the proper arguments.

- A `PythonOperator` with a `task_id` named `load` that should trigger the `load` function with the proper arguments. As explained in the Setup Instructions, you should pass a `PostgresHook` instance to the load function, and this instance should be setup with the proper `postgres_conn_id` (the one that you created).


We have already added the `transform` and `load` functions signatures, but again: **for this part, you don't have to fill the functions but only to create the Airflow tasks that will call them.**

As for the first exercise, you should use the `AIRFLOW_HOME` environment variable to build the path of your joke json file to have both the tests and the DAG working.

The second task should be triggered only after the first one's success.
The third task should be triggered only after the first second's success.
The fourth task should be triggered only after the first third's success.

Once you are confident with your code run:
```
make test_tasks_configs
```

Once you passed the tests, launch your Airflow instance and open http://localhost:8080/home to see how your DAG looks.

You should see your four tasks. Turn the dag on and see what happens! It should be all green as your tasks called functions that do not do anything for now.

## Python Functions Instructions

To help you, we have already added the signature of 6 functions. This is now your turn to implement them in the current order.

Do not hesitate to manually trigger the DAG to see what your code does.
No need, to restart docker-compose when you change the DAG code, just refresh your browser.

If you want to see what is inside your Airflow database you need:
- to have your docker-compose running
- to open a new terminal and run the following comment:
  - ```psql -h localhost -U airflow -d db``` (and provide the password you defined in your .env)


If you want to see what is inside the test database that we use you can run:
```
sqlite3 $PWD/airflow.db
```

Once you are confident with your code run:
```
make test_python_functions
```

Now, you should be able to trigger the DAG, see green results and have your `swedified_jokes` table being filled.
