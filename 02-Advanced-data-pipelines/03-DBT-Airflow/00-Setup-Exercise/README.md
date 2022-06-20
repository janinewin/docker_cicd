# Setup Exercise


### Introduction

The goal of this exercise is to have dbt installed on Airflow and to have a DAG that triggers two commands `dbt run` and `dbt test`.

## Setup files and folders

We already created a dbt folder for you that contains the models you created previously in the week.

## Setup the Dockerfile

In order to make Airflow properly run dbt, there are several environment variables to set. Open your `Dockerfile` and add the following lines after `ENV AIRFLOW_HOME=/opt/airflow`:

```
ENV DBT_DIR=$AIRFLOW_HOME/dbt
ENV DBT_TARGET_DIR=$DBT_DIR/target
ENV DBT_PROFILES_DIR=$DBT_DIR
ENV DBT_VERSION=1.0.4
```

These lines will allow airflow to know in which folders to look up when running `dbt` commands.

## Setup the docker-compose.yml

There are not that many things to do in that part. You should just add a volume for `airflow scheduler` and `airflow webserver` to sync your local `dbt` folder to your docker container (the same as you did for `dags`, `data` & `logs`).

## Setup the DAG

Open the `dbt.py` file and add your DAG inside. It should:
- be named `dbt`
- dependent on past
- not catchup
- start from yesterday and run daily

Then you should have two tasks that run one after the other:
- a BashOperator named `dbt_run` that runs dbt models
- a BashOperator named `dbt_test` that run dbt tests
