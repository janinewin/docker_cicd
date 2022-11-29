# Track long

### Introduction

You already integrated dbt to Airflow at a project level. In this exercise, your will integrate it at a model level. This means that your goal will be to have a DAG containing one task per model (and not just two tasks as before).

To complete this task you will base your DAG on the [`manifest.json`](https://docs.getdbt.com/reference/artifacts/manifest-json) generated by dbt. As you can see by opening the `dbt_lewagon/manifest.json` that we prepared for you, this file contains all models and their dependencies.

For this exercise, you will mainly work on the `dbt_advanced.py` file as we already prepared most of the setup. You just have to recreate the same `profiles.yml` and `.env` as for the previous exercise and add `_optional` at the end of your dataset's name.

PS: We removed most of the `manifest.json` content to keep only the needed parts and make it more readable, but usually, this file contains thousands of lines.

### Setup Instructions

The `Dockerfile` and the `docker-compose.yml` are the same as the ones you used today and we have already prepared the `pyproject.toml` for you.

Make sure your terminal is in the current exercise folder and let's start by initiating a local Airflow database that will be used by `pytest` by running:

```bash
make init_db
```

As before, create an `.env` file and set `POSTGRES_PASSWORD` to the value of your choice and do not forget to add the proper volume for your `.gcp_keys` in your `docker-compose.yml`.

## Setup the DAG

Open the `dbt_advanced.py` file and add your DAG inside. It should:
- be named `dbt_advanced`
- depend on past
- not catchup
- start from yesterday and run daily

For the first time, you won't manually declare your task but you will generate them by using python functions. To help you understand this new concept, we already added for you the functions calls such that you just have to code the functions themselves.

As always, once your confident with what you have done, run the following command:

```bash
make test_dag_config
```

## Setup the python functions

As just explained, we have prepared the functions signatures and the functions calls that you will have to use. Each function also contains a description of what it is supposed to do. However, to make sure you fully understand the whole process, here is a summary:
- the `load_manifest` function will be called first and will be given the `manifest.json` path that it will load as a `dict` and return
- the returned `dict` will be given to the `create_tasks` function that will build a dict containing the `nodes` of the `manifest.json` as keys and their corresponding BashOperators as values
- these BashOperators will be built by the `make_dbt_task` function that will be called by the `create_tasks` function for each node by giving the proper dbt verb (`run` or `test`)
- the `create_dags_dependencies` function will reuse this `dict` to create the Airflow tasks. To order them properly, this function will have to manipulate the `depends_on` field of the `manifest.json`

This exercise is quite challenging to implement, so do not hesitate to check with a teacher that you have properly understood the requirements before starting.

At the end, you should have a DAG that looks like [this](https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W2D3/dbt_dag.png).

As always, once your confident with what you have done, run the following command:

```bash
make test_python_functions
```

and

```bash
make test_tasks_configs
```

Again, once done, do not hesitate to make it work with your own models.