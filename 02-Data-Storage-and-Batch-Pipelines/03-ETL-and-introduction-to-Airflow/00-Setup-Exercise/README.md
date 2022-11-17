### Introduction

The goal of this exercise is to have Airflow running through docker-compose. We already provided one file to help you (`scripts/endpoint.sh`) but you will have to handle the rest by yourselves. To build the lightest version of Airflow you need at least four components:
- a `postgres database` to store Airflow metadata
- a `webserver` to display Airflow UI
- a `scheduler` to orchestrate your future DAGs
- a `dags` folder

## Setup files and folders

1. Start by creating your `dags` folder at the root level, as required by Airflow.
2. On top of that, create two other folders `data` & `logs` (at the root level too) that Airflow will use to sync data between its container and your local setup.
3. Create a `.gitkeep` file in each of them, such that, even if they are empty, the folders will be pushed to github.
4. Once you are confident with what you've done, run the tests:

```bash
make test_files_and_folders
```

## Setup the Dockerfile

### Context and Objectives

You need to create the Dockerfile that will be used by your `webserver` and `scheduler` services. There are a lot of ways to build it, but we made our tests very strict to ensure that you all reach the same point to start the exercises of the day (that's why you could have a setup that works but that does not pass the test).

The main requirements to respect will be to:
- [set the `AIRFLOW_HOME` environment variable](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html?highlight=airflow_home#envvar-AIRFLOW_HOME)
- install the `PostgreSQL` client
- install `poetry` and its content

You could use an Airflow image to start our Dockerfile but we will keep it as light as possible and use a python image to start.

### Instructions

We will help you to build your Dockerfile through **🔟 instructions** that you will have to implement.

Let's start by creating a `Dockerfile` and make it start from a `python:3.8.10-slim` image (1️⃣).

As for your first day, set the `DEBIAN_FRONTEND` argument to `noninteractive` (2️⃣) and the `PYTHONUNBUFFERED` environment variable to `1` (3️⃣).

Then, set the environment variable `AIRFLOW_HOME` to `/opt/airflow` (4️⃣) and move your `WORKDIR` on it (5️⃣).

Now, it's time for you to take a look at the `scripts/entrypoint.sh` file that we have created for you. First, you should see a block of code that checks whether PostgreSQL is ready or not, then you should see three Airflow commands that:
- update the Airflow database
- create an Airflow user
- [start an Airflow `webserver` instance](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#webserver)

As your Airflow `webserver` will run this file, it has to know the `psql` command that comes from the `postgresql` package. We want you to use the `postgresql-14`, for which [the install is a bit more complex](https://techviewleo.com/how-to-install-postgresql-database-on-ubuntu/), which is why we will provide it to you. To properly install the `postgresql-14` package you thus have to add the following lines to your Dockerfile: (6️⃣)

```Dockerfile
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

After that, implement the two following commands:
- a copy of the `scripts` folder inside the Docker image (7️⃣)
- a bash command to make `scripts/entrypoint.sh` runnable (8️⃣)

Finally, you will have to setup `poetry`.

Start by adding a command to copy the `pyproject.toml` and the `poetry.lock` files to the Docker image (9️⃣).

Then, add a bash command that run three consecutive steps to upgrade pip (by skipping cache if it exists), install poetry and finally install poetry packages without the dev packages (🔟).

To recap the previous explanations you should have the following 🔟 commands:
- 1️⃣ a `python:3.8.10-slim` image
- 2️⃣ the `DEBIAN_FRONTEND` argument set to `noninteractive`
- 3️⃣ the `PYTHONUNBUFFERED` environment variable set to `1`
- 4️⃣ the `AIRFLOW_HOME` environment variable set to `/opt/airflow`
- 5️⃣ the `WORKDIR` set to `/opt/airflow`
- 6️⃣ a bash command to install `postgresql-14`
- 7️⃣ a copy of the `scripts` folder (to the `scripts` folder)
- 8️⃣ a bash command to make `scripts/entrypoint.sh` runnable
- 9️⃣ a copy of `pyproject.toml` and `poetry.lock` (to the root level)
- 🔟 a bash command to upgrade `pip`, use it to install `poetry` and finally install poetry content (without the dev packages)

Once you are confident with what you've done, run the tests:

```bash
make test_dockerfile
```

## Setup the docker-compose.yml

As explained above, you will create a light docker-compose with the minimal requirements, but do not hesitate to take a look to the official docker-compose.yml of Airflow [here](https://github.com/apache/airflow/blob/main/docs/apache-airflow/start/docker-compose.yaml).

Let's create a `docker-compose.yml` file and read the following sections to add the three required services:
- postgres
- an Airflow scheduler
- an Airflow webserver

### Postgres service

For your PostgreSQL service (name it postgres), you need:
- a `postgres:14` image
- 3 environment variables: `POSTGRES_DB`, `POSTGRES_PASSWORD` and `POSTGRES_USER` equal to `db`, `$POSTGRES_PASSWORD` and `airflow`
- a volumes to store PostgreSQL data into a local folder named database (`./database/:/var/lib/postgresql/data`)
- a [`healthcheck`](https://marcopeg.com/docker-compose-healthcheck/) with an `interval of 5 seconds` and `5 potential retries` that checks that your database is ready (`["CMD", "pg_isready -d db -U airflow"]`)
- a mapping of the `port 5432` to your `port 5432`
- a restart config set to `always`

You noticed that we make you set `POSTGRES_PASSWORD` to `$POSTGRES_PASSWORD`, you thus have to create an `.env` file and set `POSTGRES_PASSWORD` to the value of your choice.

### Scheduler service

For your scheduler service, you need:
- to use the `Dockerfile` that you just created (use the `build` keyword)
- to restart on `failure`
- to start only once postgres is ready
- 2 environment variables: `AIRFLOW__CORE__EXECUTOR` and `AIRFLOW__DATABASE__SQL_ALCHEMY_CONN` equal to `LocalExecutor` and `postgresql+psycopg2://airflow:$POSTGRES_PASSWORD@postgres:5432/db`
- 3 volumes to sync your `dags`, `data` and `logs` folders with Airflow ones (they should be stored at the `/opt/airflow` level on Airflow side)
- to run the command `poetry run airflow scheduler` at start

You noticed that we set your `AIRFLOW__CORE__EXECUTOR` to `LocalExecutor` as we wanted you to use a light Airflow, but in production you would use other [values](https://airflow.apache.org/docs/apache-airflow/stable/executor/index.html).

You also noticed that you defined the `AIRFLOW__DATABASE__SQL_ALCHEMY_CONN` environment variable that will allow Airflow to connect to your PostgreSQL database. [Have a look at the documentation to see all available environment variables](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html)

### Webserver service

For your scheduler service, you need:
- to use the `Dockerfile` that you just created (use the `build` keyword)
- to run the `scripts/entrypoint.sh` at start using `poetry`
- to restart on `failure`
- to start only once postgres and scheduler are ready
- 5 environment variables: the five that you already added in the previous services
- the same 3 volumes as for the scheduler
- a mapping of the `port 8080` to your `port 8080` (this will allow you to locally get the Airflow UI)
- a `healthcheck` with a `interval of 30 seconds`, `a timeout of 30s` and `3 potential retries` that checks that Airflow webserver is ready (`["CMD-SHELL", "[-f /home/airflow/airflow-webserver.pid]"]`)

Once you are confident with what you've done, run the tests:

```bash
make test_docker_compose
```

At that point, you should be able to run the following command (that will force rebuild the image of your Dockerfile and recreate your docker-compose):

```bash
docker-compose up
```

Now, visit [localhost](http://localhost:8080/home). Have a look to the `scripts/entrypoint.sh` to find the login and password to use!

👉 You should see all Airflow DAG examples! Do not hesitate to play a bit with them to get familiar with Airflow UI ✨