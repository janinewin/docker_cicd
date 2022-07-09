# Setup Exercise

### Introduction

The goal of this exercise is to have dbt installed on Airflow and to have a DAG with two tasks that trigger `dbt run` and `dbt test`.

We already created a dbt project (`dbt_lewagon`) for you that contains the models coming from `dbt init`, which will be enough to test your setup.

Make sure your terminal is in the current exercise folder and let's start by initiating a local Airflow database that will be used by `pytest` by running:

```bash
make init_db
```

## Setup files

In order to run dbt with its own configuration, Airflow needs a `profiles.yml`:
- this file should be created in the `dbt_lewagon` folder
- it should contain a `dbt_lewagon` profile with:
  - a `dev` output (and `target` should points to `dev`) with:
    - `dataset` equal to `dbt_name_day2` (Replace `name` with the first letter of your first name and your whole last name, `dbt_bobama_day2` for instance)
    - `job_execution_timeout_seconds` equal to `300`
    - `job_retries` equal to `1`
    - `location` equal to `US`
    - `method` equal to `service-account`
    - `priority` equal to `interactive`
    - `project` equal to your Google Cloud project
    - `threads` equal to `1`
    - `type` equal to `bigquery`
    - `keyfile` equal to `/opt/airflow/.gcp_keys/the_name_of_your_keyfile.json` (replace with the proper file's name of course)

Once you are confident with what you've done, run the tests:

```bash
make test_profiles_yml
```

## Setup the Dockerfile

First, let's note that we already added `dbt-core` and `dbt-bigquery` to your `pyproject.toml` (that Airflow will use). Then, there are several environment variables for Airflow to know in which folders to look up when running `dbt` commands. Open your `Dockerfile` and add the following lines after `ENV AIRFLOW_HOME=/opt/airflow`:

```
ENV DBT_DIR=$AIRFLOW_HOME/dbt_lewagon
ENV DBT_TARGET_DIR=$DBT_DIR/target
ENV DBT_PROFILES_DIR=$DBT_DIR
ENV DBT_VERSION=1.1.1
```

You may have noticed that you set `$DBT_PROFILES` to `/opt/airflow/dbt_lewagon`, which make sense as we made you create your `profiles.yml` in this folder.

Once you are confident with what you've done, run the tests:

```bash
make test_dockerfile
```

## Setup the docker-compose.yml

There are not that many things to do in that part. You should just have to add two volumes in your `airflow scheduler` to sync:
- your local `dbt_lewagon` folder to your docker container
- your local `.gcp_keys` folder to your docker container (you will probably have to set the entire path to your `.gcp_keys`, like `/Users/username/.gcp_keys:/opt/airflow/.gcp_keys`)

Once you are confident with what you've done, run the tests:

```bash
make test_docker_compose
```

Before moving to the next part, create and fill your `.env` file as usual.


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

```bash
Failure in test not_null_my_first_dbt_model_id (models/example/schema.yml)
Got 1 result, configured to fail if != 0
```

Once you are confident with what you've done, run the tests:

```bash
make test_dag_and_tasks_configs
```

As already explained, even if we did some tests to help you, the best way to verify that your setup worked, is to open your [BigQuery console](https://console.cloud.google.com/bigquery) and verify that you have a new dataset named `dbt_name_day2` that contains your two models.

# Optional Part

If you want to make sure that this setup would scale with other dbt_projects, replace the `dbt_lewagon` folder with the project that you've done in the previous day, make sure that it runs properly and go to BigQuery to check that your models have been created.
