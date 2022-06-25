# Advanced Airflow

### Introduction

In this challenge, you will implement another ETL by using advanced Airflow concepts (Sensor, xcom, BranchOperator).

The goal is to have three DAGs running every month that will:
- get the monthly New York City Taxi and Limousine Commission (NYC-TLC) data
- filter the data based on the month to only keep outliers
- load them into your PostgreSQL database

To get the NYC-TLC data, you will use their public [s3 bucket](https://nyc-tlc.s3.amazonaws.com/).
For the saving system, you will use the [parquet format](https://fr.wikipedia.org/wiki/Apache_Parquet) which is very popular in the Data Engineering world to store large amount of data without taking too much space.

### Setup Instructions

The `Dockerfile` and the `docker-compose.yml` are the same as the ones you used in the first week and we have already prepared the `pyproject.toml` for you.

Make sure your terminal is in the current exercise folder and let's start by initiating a local Airflow database that will be used by `pytest` by running:

```bash
make init_db
```

As before, create an `.env` file and set `POSTGRES_PASSWORD` to the value of your choice.

For this exercise, the process is a bit different as you will have to create three DAGs.

## Extract DAG Instructions

First, let's focus on creating the extract DAG.

You need to create a DAG with the following requirements:
- it should be named `extract`
- it should depends on past
- it should starts at `2021-06-01` and ends at `2021-12-31`
- it should run every month

Then, you need one task:
- a BashOperator named `get_parquet_data` that will curl monthly data from a s3 bucket and store it locally. The s3 bucket path is designed like this `https://nyc-tlc.s3.amazonaws.com/trip+data/yellow_tripdata_YYYY-MM.parquet` (use [airflow_variable] (https://airflow.apache.org/docs/apache-airflow/stable/templates-ref.html) to generate the date dynamically). You should save the parquet file to `bronze/yellow_tripdata_YYYY-MM`.


Once, you are confident with your code run:

```bash
make test_extract_dag
```

If this is not done yet, open an Airflow instance locally and start your DAG to download the data and inspect it. Then, move to the next part.

## Transform DAG Instructions

It's time to create the transform DAG. The main goal of this DAG is to read the parquet file you saved in `bronze`, to apply a specific operation based on the month of the data and to save the transformed data into `silver`. If the month is odd, you will only keep the long trips, otherwise you will keep the expensive ones (while using BranchOperator).

Regarding the DAG configurations, reuse the same arguments as for the `extract` one, just name the DAG `transform`.

As we want your `transform` DAG to run only once the `extract` one is done, you will have to use a [sensor](https://airflow.apache.org/docs/apache-airflow/stable/concepts/sensors.html).

You need four tasks:
- a [ExternalTaskSensor](https://airflow.apache.org/docs/apache-airflow/stable/howto/operator/external_task_sensor.html) with a `task_id` named `extract_sensor` that should wait for the DAG `extract` to be in a success state, and check its state every 10 seconds for a maximum of 10 minutes (after that it should timeout)
- a [BranchPythonOperator](https://airflow.apache.org/docs/apache-airflow/1.10.6/concepts.html?highlight=branch+operator#branching) with a `task_id` named `is_month_odd` that should trigger the `is_month_odd` function with the proper arguments
- a `PythonOperator` with a `task_id` named `filter_long_trips` that should trigger the `filter_long_trips` function with the proper arguments (set the `distance` argument to `100`)
- a `PythonOperator` with a `task_id` named `filter_expensive_trips` that should trigger the `filter_expensive_trips` function with the proper arguments (set the `amount` argument to `500`)


To help you, we have already added the `is_month_odd`, `filter_long_trips` and `filter_expensive_trips` functions signatures, but be careful:
**for this part, you don't have to fill the functions but only to create the Airflow tasks that will call them.**

We want your filtered parquet files to be saved as `silver/yellow_tripdata_2021-06.parquet` (adapt the date based on the execution date of course).

The second task should be triggered only once the first one succeeds.
The third/fourth task should be triggered based on the return of the second one.

Then, as for the previous week, you have to fill the functions that we have created for you in the proper order. Once you are confident with your code run:

```bash
make test_transform_dag
```

## Load DAG Instructions

Finally, you will have to create the `load` DAG. The main goal of this DAG is to take the data you put in `silver`, to load it into your database and print the number of inserted rows (while using xcom).

Regarding the DAG configurations, reuse the same arguments as before and just name your DAG `load`.

As we want your `load` DAG to run only once the `transform` one is done, you will have to use a `sensor` again.

You need three tasks:
- a [ExternalTaskSensor](https://airflow.apache.org/docs/apache-airflow/stable/howto/operator/external_task_sensor.html) with a `task_id` named `transform_sensor` that should wait for the DAG `transform` to be in a success state, and check its state every 10 seconds for a maximum of 10 minutes (after that it should timeout)
- a `PythonOperator` with a `task_id` named `load_to_database` that should trigger the `load_to_database` function with the proper arguments
- a `PythonOperator` with a `task_id` named `display_number_of_inserted_rows` that should trigger the `display_number_of_inserted_rows` function with the proper arguments


To help you, we have already added the `load_to_database` and `display_number_of_inserted_rows`.

The second task should be triggered only once the first one succeeds.
The third one should be triggered only once the the second one succeeds.

You probably noticed that we didn't ask you to create a task for creating the table as we did in the past. The reason is simple, this time you will use `pandas` and its [`to_sql` function](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_sql.html) that will directly create the table for you. However, to benefit from this function, you have to provide a database connection (which is different than an Airflow connection). To make it easier, we already provided a function named `create_connection_from_hook` that create a database connection from an Airflow hook and that you will have to pass to your `to_sql` function.

Moreover, as said just above, we want you to print the number of inserted rows in your second task. Until now, when you had to pass data through tasks you always save it into files. For this last task, you will use [Airflow xcom](https://airflow.apache.org/docs/apache-airflow/stable/concepts/xcoms.html) to transfer data from `load_to_database` to `display_number_of_inserted_rows`

As always, once your confident with what you have done, run the following command:

```bash
make test_load_dag
```
