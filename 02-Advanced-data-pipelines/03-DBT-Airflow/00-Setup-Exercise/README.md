# Setup Exercise

### Introduction

The goal of this exercise is to have dbt installed on Airflow and to have a DAG that triggers two commands `dbt run` and `dbt test`.

We already created a dbt project (`lewagon_dbt`) for you that contains the models coming from `dbt init`, which will be enough to test our setup.

We also provided a python script (`create_airflow_service_account_json.py`) that can generate a `service_account.json` from environment variables. The main purpose of this script is to avoid copying your own `service_account.json` to Airflow which could lead to security issues (such as pushing your `service_account.json` to Github).

Finally, we also replaced the usual `entrypoint.sh` file to `webserver_entrypoint.sh` and created a dedicated one for your scheduler (`scheduler_entrypoint.sh`).

In order to have dbt running on Airflow, there are several things to do on your side:
- create and fill your `profiles.yml`
- update the `Dockerfile` to set the needed environment variables
- update the `docker-compose.yml` to sync the `lewagon_dbt` folder with your Airflow container and load environment variables
- create a DAG that runs dbt commands


## Setup files

In order to run dbt, Airflow needs a `profiles.yml`:
- this file should be created in the `lewagon_dbt` folder
- it should contain a `dev` target with:
    - `dataset` equal to `dbt_basics_airflow`
    - `job_execution_timeout_seconds` equal to `300`
    - `job_retries` equal to `1`
    - `location` equal to `US`
    - `method` equal to `service-`account`
    - `priority` equal to `interactive`
    - `project` equal to your Bigquery staging dev project (for instance: `lewagon-dev-stg-353917`)
    - `threads` equal to `1`
    - `type` equal to `bigquery`

You probably have noticed that the value for `keyfile` was not given above: this is your role to set it to the proper path (**WARNING** you don't have to create any file for that, as explained, the file will be created for you by one of the scripts we added. Your role here is just to provide the proper path to that file).

Once you are confident with what you've done, run the tests:

```bash
make test_profiles_yml
```


## Setup the Dockerfile

First, let's note that we already added `dbt-core` and `dbt-bigquery` to your `pyproject.toml` (that Airflow will use). Then, as explained above, there are several environment variables to set. Open your `Dockerfile` and add the following lines after `ENV AIRFLOW_HOME=/opt/airflow`:

```
ENV DBT_DIR=$AIRFLOW_HOME/lewagon_dbt
ENV DBT_TARGET_DIR=$DBT_DIR/target
ENV DBT_PROFILES_DIR=$DBT_DIR
ENV DBT_VERSION=1.1.1
```

These lines will allow Airflow to know in which folders to look up when running `dbt` commands. You may have noticed that we set `$DBT_PROFILES` to `$DBT_DIR` which explains why the `profiles.yml` that Airflow will use should be stored in `$DBT_DIR`. Then, we need you to add a command to create a `.bigquery_keys` folder in which the `service-account.json` will be created. In so doing, add the following line to your `Dockerfile` (put it just after lines that you just added to keep all dbt commands at the same place):

```
RUN mkdir -p $AIRFLOW_HOME/.bigquery_keys
```

Once you are confident with what you've done, run the tests:

```bash
make test_dockerfile
```

PS: Take time to notice that we slightly updated the `Dockerfile` to run our two different endpoint scripts.

## Setup the docker-compose.yml

There are not that many things to do in that part. You should just add one volume for `airflow scheduler` and `airflow webserver` to sync your local `dbt` folder to your docker container (the same as you did for `dags`, `data` & `logs`).


Once you are confident with what you've done, run the tests:

```bash
make test_docker_compose
```

Take time to notice that we added several environment variables for your `scheduler`. The environment variables will be used in the `create_airflow_service_account_json.py` script that is called by the new `scripts/scheduler_endpoint.sh` (that is itself called by the `scheduler` service in your `docker-compose.yml`).

Before moving to the next part, create and fill your `.env` file by following the `env-template` requirements. For this day, we won't ask you to create another `service-account`, just reuse the credentials that you already have in your `~/.bigquery_keys/student-dev-service-account.json` to correctly fill your `.env`.


## Setup the DAG

Open the `dbt_basics.py` file and add your DAG inside. It should:
- be named `dbt_basics`
- depend on past
- not catchup
- start from yesterday and run daily

Then you should have two tasks that run one after the other:
- a BashOperator named `dbt_run` that runs dbt models, be careful, [you will have to specify the dbt_dir folder](https://docs.getdbt.com/dbt-cli/configure-your-profile#advanced-customizing-a-profile-directory)
- a BashOperator named `dbt_test` that run dbt tests, be careful, [you will have to specify the dbt_dir folder](https://docs.getdbt.com/dbt-cli/configure-your-profile#advanced-customizing-a-profile-directory)

When running this DAG, you should have the `dbt_test` failing, but this is normal, remember that this is how the `dbt_init` was built. However, make sure that the error you have is the expected one:

```
Failure in test not_null_my_first_dbt_model_id (models/example/schema.yml)
Got 1 result, configured to fail if != 0
```

Once you are confident with what you've done, run the tests:

```bash
make test_dag_and_tasks_configs
```

As already explained, even if we did some tests to help you, the best way to verify that your setup worked is to open your [BigQuery console](https://console.cloud.google.com/bigquery) and verify that you have a new dataset named `dbt_basics_airflow` that contains your two models.
