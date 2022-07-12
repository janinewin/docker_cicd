# Advanced Airflow

### Introduction

In this challenge, you will implement a more complex ETL by using advanced Airflow concepts (`Sensor`, `BranchOperator`, `Templating`, `trigger_rule` & `idempotency`) and a data engineering's architecture (`bronze / silver`, `Google Cloud Storage`, `BigQuery`).

The goal is to have three DAGs running every month that will:
- download the monthly New York City Taxi and Limousine Commission (NYC-TLC) data
- filter the data based on the month to only keep outliers
- load the filtered data into both, your Data Lake and your Data Warehouse (`Google Cloud Storage` and `BigQuery`)

To get the NYC-TLC data, you will use their public [data](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page).
For the saving system, you will use the parquet format for your bronze layer and the csv format for your silver one.

### Setup Instructions

The `Dockerfile` and the `docker-compose.yml` are the same as the ones you used in the first week and we have already prepared the `pyproject.toml` for you.

Make sure your terminal is in the current exercise folder and let's start by initiating a local Airflow database that will be used by `pytest` by running:

```bash
make init_db
```

As before, create an `.env` file and set `POSTGRES_PASSWORD` to the value of your choice.

As your three DAGs should have the same config, we already provided them to you. For each of them, you will follow the same process:
- create the required tasks
- fill the functions already provided (if there are some)
- test locally by running the Airflow instance and launching your dags
- run the tests

## Extract DAG Instructions

First, let's focus on creating the `extract` DAG.

You should have in your `extract.py` file a DAG with the following requirements:
- it should be named `extract`
- it should depend on past
- it should start at `2021-06-01` and end at `2021-12-31`
- it should run every month

Then, you need one task:
- a BashOperator named `curl_trip_data` that will curl monthly data from a s3 bucket and store it locally. The s3 bucket path is designed like this `https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_YYYY-MM.parquet` (use [airflow_variable](https://airflow.apache.org/docs/apache-airflow/stable/templates-ref.html) to generate the date dynamically). You should save the parquet file to `/opt/airflow/data/bronze/yellow_tripdata_YYYY-MM.parquet`.


Once, you are confident with your code run:

```bash
make test_extract_dag
```

You will see that the tests fake running your DAG on two dates `2021-06-01` and `2021-07-01` to make sure that you correctly use Airflow's variables.

If this is not done yet, open an Airflow instance locally and start your DAG to download the data and make sure that it is appearing in your folder.

💾 Save your work in progress on GitHub

## Transform DAG Instructions

It's time to play with the `transform` DAG. The main goal of this DAG is to read the parquet file you saved in `bronze`, to apply a specific operation based on the month of the data and to save the transformed data into `silver`. If the month is odd, you will only keep the long trips, otherwise you will keep the expensive ones (while using BranchOperator). But before implementing the functions, let's focus on the tasks.

As we want your `transform` DAG to run only once the `extract` one is done, you will have to use a [sensor](https://airflow.apache.org/docs/apache-airflow/stable/concepts/sensors.html).

You need five tasks:
- a [ExternalTaskSensor](https://airflow.apache.org/docs/apache-airflow/stable/howto/operator/external_task_sensor.html) with a `task_id` named `extract_sensor` that should wait for the DAG `extract` to be in the `success` state, and check its state every 10 seconds for a maximum of 10 minutes (after that, it should timeout). No need, to specify an external `task_id`, such that it will wait for the DAG itself to succeed
- a [BranchPythonOperator](https://airflow.apache.org/docs/apache-airflow/1.10.6/concepts.html?highlight=branch+operator#branching) with a `task_id` named `is_month_odd` that should trigger the `is_month_odd` function with the proper arguments
- a `PythonOperator` with a `task_id` named `filter_long_trips` that should trigger the `filter_long_trips` function with the proper arguments (set the `distance` argument to `150`)
- a `PythonOperator` with a `task_id` named `filter_expensive_trips` that should trigger the `filter_expensive_trips` function with the proper arguments (set the `amount` argument to `500`)
- a `EmptyOperator` with a `task_id` named `end`

To help you, we have already added the `is_month_odd`, `filter_long_trips`, `filter_expensive_trips` and functions signatures, but be careful:
**for this part, you don't have to fill the functions but only to create the Airflow tasks that will call them.**

We want your filtered parquet files to be saved as `/opt/airflow/data/silver/yellow_tripdata_YYYY-MM.csv` (adapt the date based on the execution date of course).

The second task should be triggered only once the first one succeeds.
The third or the fourth task should be triggered based on the return of the second one.
The fifth task should be triggered only once the third/fourth one succeeds.

As the fifth task should be triggered as soon as one of the third/fourth task is successful (only one of both will run), let's set its trigger_rule to [`one_success`](https://airflow.apache.org/docs/apache-airflow/1.10.5/concepts.html?highlight=trigger+rule#trigger-rules). If you wonder why we added an EmptyOperator at the end, this is just to have a single task closing your DAG and not two distinct branches which is more visual.

Then, as for the previous week, you have to fill the functions that we have created for you in the proper order. Once you are confident with your code run:

```bash
make test_transform_dag
```

Again, run the DAG on your Airflow UI to check that everything is running well and then save your work in progress on GitHub.

## Load DAG Instructions

Finally, you will have to create the `load` DAG. The main goal of this DAG is to take the data you put in `silver` and to load it into `Google Cloud Storage` and then `BigQuery`.

In order to use BigQuery you will have to create the Airflow connection. This time, you will do it directly from the Airflow UI.

Once you have a local Airflow instance running, hover the `Admin` tab and select `Connections`. Click on the white cross to add a new record:
- name the `Connection Id` `google_cloud_connection`
- set the `Connection Type` to `Google Cloud`
- copy paste the whole content of your `service-account.json` to the `Keyfile JSON`

To make your life easier, you will use the `GCSToBigQueryOperator` that will allow you to directly load file from Google Cloud Storage to BigQuery without using a hook. In order to use it, you need to push your local data to Google Cloud Storage.

In so doing:
- open your google cloud console
- go to Google Cloud Storage
- create a bucket named `name-silver` (once again, replace with your first letter of first name and whole last name) and let the default parameters for that bucket

Once the bucket creation is done, let's move to your DAG.

This branch needs 6 tasks:
- an [ExternalTaskSensor](https://airflow.apache.org/docs/apache-airflow/stable/howto/operator/external_task_sensor.html) with a `task_id` named `transform_sensor` that should wait for the DAG `transform` to be in the `success` state, and check its state every 10 seconds for a maximum of 10 minutes (after that it should timeout)
- a [LocalFileSystemToGCSOperator](https://airflow.apache.org/docs/apache-airflow-providers-google/1.0.0/operators/transfer/local_to_gcs.html) with a `task_id` named `upload_local_file_to_gcs` that should load your local silver file to your Google Cloud Storage silver bucket with the same file's name
- a [`BigQueryCreateEmptyDatasetOperator`](https://airflow.apache.org/docs/apache-airflow-providers-google/stable/_api/airflow/providers/google/cloud/operators/bigquery/index.html#airflow.providers.google.cloud.operators.bigquery.BigQueryCreateEmptyDatasetOperator) with a `task_id` named `create_dataset` that should create the `name_tripdata` dataset (once again, replace with the first letter of your first name and your whole last name)
- a [`BigQueryCreateEmptyTableOperator`](https://airflow.apache.org/docs/apache-airflow-providers-google/stable/_api/airflow/providers/google/cloud/operators/bigquery/index.html#airflow.providers.google.cloud.operators.bigquery.BigQueryCreateEmptyTableOperator) with a `task_id` named `create_table` that should create a table named `trips` (once again, replace with the first letter of your first name and your whole last name) in the dataset `name_tripdata` with the proper schema (`month` as a string and `trip_distance` & `total_amount` as floats)
- a [BigQueryInsertJobOperator](https://airflow.apache.org/docs/apache-airflow-providers-google/stable/_api/airflow/providers/google/cloud/operators/bigquery/index.html#airflow.providers.google.cloud.operators.bigquery.BigQueryInsertJobOperator) with a `task_id` name `remove_existing_data` that should run a query to remove data at the current date (in order to be idempotent)
- a [`GCSToBigQueryOperator`](https://airflow.apache.org/docs/apache-airflow-providers-google/stable/_api/airflow/providers/google/cloud/transfers/gcs_to_bigquery/index.html) with a `task_id` named `load_to_bigquery` that should append the content of the `silver` file to the `trips` table

All tasks should be triggered in that order as soon as the previous one succeeded.

Once your confident with what you have done, run the following command:

```bash
make test_load_dag
```

WARNING: No to help you too much, we decided not to test everything in your tasks. This means that you need to manually launch the DAG and see if data is coming into your Google Cloud Storage & BigQuery instances and to update a bit your tasks if needed.

<details>
  <summary markdown='span'>💡 Hint</summary>
  You may need to set `useLegacySql` for the task_id `remove_existing_data`
  You may need to set `skip_leading_rows` & `write_disposition` for the task_id `load_to_bigquery`
</details>
