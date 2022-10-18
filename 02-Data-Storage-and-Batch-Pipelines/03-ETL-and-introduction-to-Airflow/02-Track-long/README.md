# Local ETL

In the previous track-long sessions, you have:

- set up a base `docker-compose` with `PostgreSQL`, `FastAPI` and `Adminer`
- loaded a data schema mapping the [the movies dataset](https://www.kaggle.com/rounakbanik/the-movies-dataset)
- added a Jupyter lab environment to interact with the datasets and propose a new normalized SQL schema

In today's track long exercise, we'll create a small ETL to load new comments about the movies that we have previously added to the database.

## Desired outcome

In this challenge, you will create a local E(xtract)T(ransform)L(oad).

The goal is to have a DAG running every five minutes that will:
- fetch 5 comments from an API (Extract)
- replace every single quote by two single quotes (Transform)
- insert comments into your PostgreSQL database (Load)

For the comments, you will use a home made API] that takes one url argument (`n`) and return the corresponding number of comments. For instance, if you want to retrieve the last 5 comments, call: [https://moviecomment-zxzcpvr6hq-ew.a.run.app/latest-comments?n=5](https://moviecomment-zxzcpvr6hq-ew.a.run.app/latest-comments?n=5)

PS: The reason why you will have to double the single quote is to respect PostgreSQL constraint.

### Setup Instructions

As explained above, you will have to interact with your PostgreSQL database from your DAG. To do so, you will use the [PostgresHook class](https://airflow.apache.org/docs/apache-airflow-providers-postgres/stable/_api/airflow/providers/postgres/hooks/postgres/index.html#module-airflow.providers.postgres.hooks.postgres). As you can see by reading the documentation, when instantiating a PostgresHook, you have to pass a `connection_id` corresponding to the [Airflow connection](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html) that you want to use. The first step is thus to create an Airflow connection to your database.

To create this connection, you will have to create a file named `scripts/init_connections.sh` (we have slightly updated the `Dockerfile` & `docker-compose.yml` to run this file). Then copy paste the following lines in your `scripts/init_connections.sh`:

```bash
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

As you can see, we use the Airflow command line interface to create a connection named `postgres_connection` that is built from your database's configuration.

Apart from that, the `Dockerfile` and the `docker-compose.yml` are the same as the ones you created in the setup exercise, and we have already prepared the `pyproject.toml` for you.

Make sure your terminal is in the current exercise folder and let's start by creating a local Airflow database for `pytest` by running:

```bash
make init_db
```

It should create the three same files as for the previous exercise and an Airflow connection to this database (that will be used in the tests only). If you inspect the test files, you could see that we use a `sqlite` database to test your functions and not a `PostgreSQL`. We do that, because a `sqlite` database is much lighter and is stored in a simple file, which makes the tests easier to setup.

As before, create an `.env` file and set `POSTGRES_PASSWORD` to the value of your choice.

Take time to open the `dags/track_long.py` and discover the functions signatures that we have added to help you.

## DAG Instructions

First, let's focus on creating the proper DAG configuration (no tasks or python functions needed for now).

You need to create a dag with the following requirements:
- it should be named `track_long`
- it should have a start date equal to yesterday
- it should have a description saying `A simple to DAG to fetch and load last movies' comments`
- it should not catchup the missing runs
- it should be scheduled to run every 5 minutes
- it should run no matter if the previous runs succeed

Once, you are confident with your code run:
```bash
make test_dag_config
```

## Tasks Instructions

Then, we want you to create the tasks that your DAG will use.

You need two tasks:

- A [PostgresOperator](https://airflow.apache.org/docs/apache-airflow-providers-postgres/stable/_api/airflow/providers/postgres/operators/postgres/index.html#module-airflow.providers.postgres.operators.postgres) with a `task_id` named `create_comments_table` that should create a table named comments with four columns (`id`, `movie_id`, `comment` and `rating` that should be a `primary key`, a not null `integer` column, a not null `varchar` column and a not null `integer` column again).
- A `PythonOperator` with a `task_id` named `get_and_insert_last_comments` that should trigger the `get_and_insert_last_comments` function with the proper arguments.

As explained in the Setup Instructions, you should pass a `PostgresHook` instance to the `get_and_insert_last_comments` function, and this hook should be setup with the proper `postgres_conn_id` (the one that you created).

We have already added the `get_and_insert_last_comments` function signature, but again: **for this part, you don't have to fill the function but only to create the Airflow tasks that will call it.**

The second task should be triggered only after the first one's success.

Once you are confident with your code run:

```bash
make test_tasks_configs
```

Once you passed the tests, launch your Airflow instance and open [localhost](http://localhost:8080/home) to see how your DAG looks.

You should see your four tasks. Turn the dag on and see what happens! It should be all green as your tasks called functions that do not do anything for now.

## Python Functions Instructions

As for the previous exercise, we have added the signatures of 4 functions. This is your turn to implement them in the current order. As describe in the functions signatures, this DAG is not idempotent, but this is on purpose, we will address that aspect during the livecode.

Do not hesitate to manually trigger the DAG to see what your code does.
No need, to restart docker-compose when you change the DAG code, just refresh your browser.

If you want to see what is inside your Airflow database you need to add an Adminer service to your `docker-compose.yml` (use another port than the `8080` that is already used by Airflow) and to use the database configuration that you passed to your postgres service.


If you want to see what is inside the test database that we use you can run:
```bash
sqlite3 $PWD/airflow.db
```


Once you are confident with your code run:
```bash
make test_python_functions
```

Now, you should be able to trigger the DAG, see green results and have your `comments` table being filled.
