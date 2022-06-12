# Setup Exercise


### Introduction

The goal of this exercise is to have Airflow running through docker-compose. We already provided one file to help you (`scripts/endpoint.sh`) but you will have to handle the rest by yourselves. To build the lightest version of Airflow you need at least four components:
- a `postgres database` to store Airflow metadata
- a `webserver` to display Airflow UI
- a `scheduler` to orchestrate our future DAGs
- a `dags` folder

## Setup files and folders

Start by creating our `dags` folder at the root level as required by Airflow. On top of that, create two other folders (data, logs) (at the root level too) that Airflow will use to sync data between its container and your local setup.
Create a `.gitkeep` file in each of them such that even if they are empty they will be pushed to github. Once you are confident with what you've done, run the tests:

```
make test_files_and_folders
```

## Setup dockerfile

Then, you need to create the Dockerfile that will be used by your `webserver` and `scheduler` services.

The main requirements to respect are:
- [setting the `AIRFLOW_HOME` environment variable](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html?highlight=airflow_home#envvar-AIRFLOW_HOME)
- installing the `PostgreSQL` client
- installing `poetry` and its content

We could use an Airflow image to start our Dockerfile but we will keep it as simple as possible and use a light python version.

In so doing, let's start by creating a `Dockerfile`, make it start from a `python:3.8.12-slim` image, and add the usual `DEBIAN_FRONTEND` argument and `PYTHONUNBUFFERED` environment variable set to `noninteractive` and `1`. Then, set the environment variable `AIRFLOW_HOME` to `/opt/airflow` and use it as your `WORKDIR`.

Now, it's time for you to have a look to the `scripts/entrypoint.sh` file that we have created for you. First, you should see a block of code that checks whether PostgreSQL is ready or not. Then you should see three Airflow commands that:
- update the Airflow database
- create an Airflow user
- [start an Airflow `webserver` instance](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#webserver)

Our Airflow `webserver` will have to run this file. To be able to run this file, your webserver must know the `psql` command that comes from the `postgresql` package. As we want to have the version 14, [the install is a bit more complex](https://techviewleo.com/how-to-install-postgresql-database-on-ubuntu/) than usual, which is why we will provide it to you. To properly install the `postgresql-14` package you will have to add the following lines to your Dockerfile:

```
RUN apt-get update \
    && apt-get -y upgrade \
    && apt-get -y install gnupg2 wget lsb-release\
    && sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list' \
    && wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - \
    && apt-get update \
    && apt-get -y install curl postgresql-14 postgresql-contrib \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
```

Let's go back to your Dockerfile and add two new commands (after the one we provided to you just above):
- a copy of the `scripts` folder
- a bash command to make `scripts/entrypoint.sh` runnable

Finally, you will have to setup `poetry`. Start by copying the `pyproject.toml` and the `poetry.lock` files. Then, add a bash command that run three consecutive steps to upgrade pip, install poetry and finally install poetry packages without the dev packages.

To recap the previous explanations you should have the following 10 commands:
- a `python:3.8.12-slim` image
- the `DEBIAN_FRONTEND` argument set to `noninteractive`
- the `PYTHONUNBUFFERED` environment variable set to `1`
- the `AIRFLOW_HOME` environment variable set to `/opt/airflow`
- the `WORKDIR` set to `/opt/airflow`
- a bash command to install `postgresql-14`
- a copy of the `scripts` folder (to the `scripts` folder)
- a bash command to make `scripts/entrypoint.sh` runnable
- a copy of `pyproject.toml` and `poetry.lock` (to the root level)
- a bash command to upgrade `pip3`, use it to install `poetry` and finally install poetry content (without the dev packages)

Once you are confident with what you've done, run the tests:
```
make test_dockerfile
```

## Setup docker compose

As explained above, to make things easy you will create a light docker-compose with the minimal requirements, but you can have a look to the official docker-compose of Airflow here: https://github.com/apache/airflow/blob/main/docs/apache-airflow/start/docker-compose.yaml

First, let's create a docker-compose.yml file and read the following sections to add the three required services:
- postgres
- an Airflow scheduler
- an Airflow webserver

### Postgres service

For your PostgreSQL service (name it postgres), you need:
- a `postgres:14 image`
- 3 env variables: `POSTGRES_DB`, `POSTGRES_PASSWORD` and `POSTGRES_USER` equal to `db`, `$POSTGRES_PASSWORD` and `airflow`
- a volumes to store PostgreSQL data into a local folder named database (`./database/:/var/lib/postgresql/data`)
- a `healthcheck` with an `interval of 5 seconds` and `5 potential retries` that checks that our database is ready (`["CMD", "pg_isready -d db -U airflow"]`)
- a mapping of the `port 5432` to your `port 5432`
- a restart config set to `always`

You noticed that we used `$POSTGRES_PASSWORD` as our `POSTGRES_PASSWORD`, you thus have to create an `.env` file and set `POSTGRES_PASSWORD` to the value of your choice. We defined an `healtcheck` as you need this service to be up in order to run the other ones.

### Scheduler service

For your scheduler service, you need:
- to use the `dockerfile` that you just created (use the build keyword)
- to restart on `failure`
- to start only once postgres is ready
- 2 environment variables: `AIRFLOW__CORE__EXECUTOR` and `AIRFLOW__DATABASE__SQL_ALCHEMY_CONN` equal to `LocalExecutor` and `postgresql+psycopg2://airflow:$POSTGRES_PASSWORD@postgres:5432/db`
- 3 volumes to sync our `dags`, `data` and `logs` folders with Airflow ones (they should be stored at `/opt/airflow` on Airflow side)
- to run the command `poetry run airflow scheduler` at start

You noticed that we set our `AIRFLOW__CORE__EXECUTOR` to `LocalExecutor` as we wanted the lightest version of Airflow, but in production you would use other values (https://airflow.apache.org/docs/apache-airflow/stable/executor/index.html).

You also noticed that we defined the `AIRFLOW__DATABASE__SQL_ALCHEMY_CONN` environment variable that will allow Airflow to connect to our PostgreSQL database. Have a look at the documentation to see all available environment variables (https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html)

### Webserver service

For your scheduler service, you need:
- to use the `dockerfile` that you just created (use the build keyword)
- to run the `scripts/entrypoint.sh` at start using `poetry`
- to restart on `failure`
- to start only once postgres and scheduler are ready
- 5 environment variables: the five that you already added in the previous services
- the same 3 volumes as for the scheduler
- a mapping of the `port 8080` to your `port 8080` (this will allow you to locally get the Airflow UI)
- an `healthcheck` with a `interval of 30 seconds`, `a timeout of 30s` and `3 potential retries` that checks that Airflow webserver is ready (`["CMD-SHELL", "[ -f /home/airflow/airflow-webserver.pid ]"]`)

```
make test_docker_compose
```

At that point you should be able to run the following command:

```
docker-compose up --force-recreate --remove-orphans --build
```

and visit http://localhost:8080/home. Have a look to the `scripts/entrypoint.sh` to find the login and password to use!
