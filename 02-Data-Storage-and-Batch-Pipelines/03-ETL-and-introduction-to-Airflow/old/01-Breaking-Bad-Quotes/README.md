### Introduction

In this challenge, you will learn how to create a simple Airflow DAG.

The goal is to have a DAG running every five minutes that will:
- request a generator of "Breaking Bad" 🎥 quotes
- save the received quote (only if this quote has not been saved yet)

For the quotes generator, you will use this [api](https://breakingbadquotes.xyz/).

For the saving system, you will use a CSV file. [This kind of files could be considered as databases in development environments](https://en.wikipedia.org/wiki/Comma-separated_values).

We split the instructions in four parts to help you create the needed DAG.

### Setup Instructions

The `Dockerfile` and the `docker-compose.yml` are the same as the ones you created in the setup exercise (we just set the `AIRFLOW__CORE__LOAD_EXAMPLES` to `false`), and have prepared the `pyproject.toml` for you.

Make sure your terminal is in the current exercise folder and let's start by initiating a local Airflow database that will be used by `pytest` by running:

```bash
make init_db
```

It should create three files in your project:
- airflow.db
- airflow.cfg
- webserver_config.py

These files are created at your project level thanks to the `AIRFLOW_HOME=${PWD}` from the `make` command. You won't interact with those files, but they are required to setup the test environment. You will see that we often override the the value of `AIRFLOW_HOME` (default value is `~/airflow`) to `${PWD}`. This is required as you will have different Airflow instances running on your laptop (one per exercise) and don't want to mix their databases.

As before, create an `.env` file and set `POSTGRES_PASSWORD` to the value of your choice.

Take time to open the `dags/breaking_bad_quote.py` and discover the functions' signatures that we have added to help you.

## DAG Instructions

First, let's focus on creating the proper DAG configuration (no tasks or python functions needed for now).

You need to create a DAG with the following requirements:
- it should be named `breaking_bad_quotes`
- it should have a start date equal to yesterday (be careful, Airflow is expecting a datetime object)
- it should have a description saying `A simple DAG to store breaking bad quotes`
- it should not catchup the missing runs
- it should be scheduled to run every 5 minutes
- it should run no matter if the previous runs failed

Once, you are confident with your code run:
```bash
make test_dag_config
```

If you have some `Airflow Depreciation warnings` in your tests this is normal, you should just make sure not to have errors.

## Tasks Instructions

Then, you have to create the tasks that your DAG will use.

As we want your quotes to be saved in a specific CSV file, your DAG needs a task to create the file. Then, it needs another task to request a quote and save it if this is a new one.

You thus need two tasks:
- a [PythonOperator](https://airflow.apache.org/docs/apache-airflow/2.2.0/howto/operator/python.html) with a `task_id` named `create_file_if_not_exist` that should trigger the `create_file_if_not_exist` function with the proper arguments. Note, that we explicitly gave you the link to PythonOperator for Airflow 2.2.0 even if we use the 2.3.0, as we want you to use this style for now and not to confuse you with the new style that is quite different to the other Airflow operators.
- a `PythonOperator` with a `task_id` named `get_quote_and_save_if_new` that should trigger the `get_quote_and_save_if_new` function with the proper arguments

To help you, we have already added the `create_file_if_not_exist` and `get_quote_and_save_if_new` functions signatures, but be careful:
**for this part, you don't have to fill the functions but only to create the Airflow tasks that will call them.**

We want your quotes to be saved to `/app/airflow/data/quotes.csv`.

The second task should be triggered only once the first one succeeds.

Once you are confident with your code run:
```bash
make test_tasks_configs
```

Once you passed the tests, start your docker-compose:
```bash
docker-compose up
```

Finally, open [your localhost](http://localhost:8080/home) to see how your DAG looks.

You should see your two tasks. Turn the dag on and see what happens! It should be all green as your tasks called functions that do not do anything for now.

## Python Functions Instructions

To help you, we have already added the signature of 5 functions. This is now your turn to implement them in the current order. You should not have to create any other python functions but will probably have to read the followings documentations:
- [https://docs.python.org/3.8/library/csv.html](https://docs.python.org/3.8/library/csv.html)
- [https://fr.python-requests.org/en/latest/](https://pypi.org/project/requests/)

Do not hesitate to manually trigger the DAG to see what your code does.
No need to restart your `docker-compose` when you change the DAG code, just refresh your browser.

If you need to restart from a clean base, you can empty your local `data/quotes.csv` file (it is synced with the one that Airflow uses).

Once you are confident with your code run:
```bash
make test_python_functions
```

Now, you should be able to trigger the DAG, see green results and have your `quotes.csv` being filled.
