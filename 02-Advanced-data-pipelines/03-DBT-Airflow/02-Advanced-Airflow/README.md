# Advanced Airflow

### Introduction

In this challenge, you will implement a more complex ETL by using advanced Airflow concepts (`Sensor`, `BranchOperator`, `Templating`, `trigger_rule`, `xcoms` & `idempotency`).

The goal is to have three DAGs running every month that will:
- download the monthly New York City Taxi and Limousine Commission (NYC-TLC) data
- filter the data based on the month to only keep outliers
- load the filtered data into your database

To get the NYC-TLC data, you will use their public [data](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page).
For the saving system, you will use the parquet format for your bronze layer and the csv format for your silver one.

PS: We also added an optional part in which you will have to load your data into Google Cloud Storage and then BigQuery.

### Setup Instructions

The `Dockerfile` and the `docker-compose.yml` are the same as the ones you used in the first week and we have already prepared the `pyproject.toml` for you.

Make sure your terminal is in the current exercise folder and let's start by initiating a local Airflow database that will be used by `pytest` by running:

```bash
make init_db
```

As before, create an `.env` file and set `POSTGRES_PASSWORD` to the value of your choice.

As your three DAGs should have the same config, we already provided them to you.

PS: You may have noticed that in the `tests/scripts/init_connections.sh` we added a `google_cloud_connection` with a few arguments. In fact, it won't be used and wouldn't work if you tried to use it, but to avoid errors when running the optional tests, you need to have this fake connection.

## Extract DAG Instructions

First, let's focus on creating the extract DAG.

You should have in your `extract.py` file a DAG with the following requirements:
- it should be named `extract`
- it should depends on past
- it should starts at `2021-06-01` and ends at `2021-12-31`
- it should run every month

Then, you need one task:
- a BashOperator named `curl_trip_data` that will curl monthly data from a s3 bucket and store it locally. The s3 bucket path is designed like this `https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_YYYY-MM.parquet` (use [airflow_variable](https://airflow.apache.org/docs/apache-airflow/stable/templates-ref.html) to generate the date dynamically). You should save the parquet file to `/opt/airflow/data/bronze/yellow_tripdata_YYYY-MM.parquet`.


Once, you are confident with your code run:

```bash
make test_extract_dag
```

You will see that the tests fake running your DAG on two dates `2021-06-01` and `2021-07-01` to make sure that you correctly use Airflow's variables.

If this is not done yet, open an Airflow instance locally and start your DAG to download the data and make sure that it is appearing in your bucket.

💾 Save your work in progress on GitHub

## Transform DAG Instructions

It's time to create the transform DAG. The main goal of this DAG is to read the parquet file you saved in `bronze`, to apply a specific operation based on the month of the data and to save the transformed data into `silver`. If the month is odd, you will only keep the long trips, otherwise you will keep the expensive ones (while using BranchOperator).

Regarding the DAG configurations, it should reuse the same arguments as for the `extract` one, but just named `transform`.

As we want your `transform` DAG to run only once the `extract` one is done, you will have to use a [sensor](https://airflow.apache.org/docs/apache-airflow/stable/concepts/sensors.html).

You need six tasks:
- a [ExternalTaskSensor](https://airflow.apache.org/docs/apache-airflow/stable/howto/operator/external_task_sensor.html) with a `task_id` named `extract_sensor` that should wait for the DAG `extract` to be in a success state, and check its state every 10 seconds for a maximum of 10 minutes (after that, it should timeout). No need, to specify an external `task_id`, such that it will wait for the DAG itself to succeed
- a [BranchPythonOperator](https://airflow.apache.org/docs/apache-airflow/1.10.6/concepts.html?highlight=branch+operator#branching) with a `task_id` named `is_month_odd` that should trigger the `is_month_odd` function with the proper arguments
- a `PythonOperator` with a `task_id` named `filter_long_trips` that should trigger the `filter_long_trips` function with the proper arguments (set the `distance` argument to `150`)
- a `PythonOperator` with a `task_id` named `filter_expensive_trips` that should trigger the `filter_expensive_trips` function with the proper arguments (set the `amount` argument to `500`)
- a `PythonOperator` with a `task_id` named `display_number_of_kept_rows` that should trigger the `display_number_of_kept_rows` function with the proper arguments
- a `EmptyOperator` with a `task_id` named `end`

To help you, we have already added the `is_month_odd`, `filter_long_trips`, `filter_expensive_trips` and `display_number_of_kept_rows` functions signatures, but be careful:
**for this part, you don't have to fill the functions but only to create the Airflow tasks that will call them.**

We want your filtered parquet files to be saved as `/opt/airflow/data/silver/yellow_tripdata_YYYY-MM.csv` (adapt the date based on the execution date of course).

The second task should be triggered only once the first one succeeds.
The third/fourth task should be triggered based on the return of the second one.

As the fifth task should be triggered as soon as one of the third/fourth task is successful (only one of both will run), let's set its trigger_rule to [`one_success`](https://airflow.apache.org/docs/apache-airflow/1.10.5/concepts.html?highlight=trigger+rule#trigger-rules). If you wonder why we added an EmptyOperator at the end, this is just to have a single task closing your DAG and not two distinct branches which is more visual.

Then, as for the previous week, you have to fill the functions that we have created for you in the proper order. Once you are confident with your code run:

```bash
make test_transform_dag
```

Again, run the DAG on your Airflow UI to check that everything is running well and then save your work in progress on GitHub.

## Load DAG Instructions

Finally, you will have to create the `load` DAG. The main goal of this DAG is to take the data you put in `silver` and to load it into your database and print the number of inserted rows (while using `xcom`).

As we want your `load` DAG to run only once the `transform` one is done, you will have to use a `sensor` again.

You need four tasks:
- an [ExternalTaskSensor](https://airflow.apache.org/docs/apache-airflow/stable/howto/operator/external_task_sensor.html) with a `task_id` named `transform_sensor` that should wait for the DAG `transform` to be in a success state, and check its state every 10 seconds for a maximum of 10 minutes (after that it should timeout)
- a `PosgtresOperator` with a `task_id` named `create_trips_table` that should create a table named `trips` with three columns (`date`, `trip_distance` and `total_amount` that should be a not null `varchar` column, two not null `real` columns).
- a `PythonOperator` with a `task_id` named `load_to_database` that should trigger the `load_to_database` function with the proper arguments
- a `PythonOperator` with a `task_id` named `display_number_of_inserted_rows` that should trigger the `display_number_of_inserted_rows` function with the proper arguments

To help you, we have already added the `load_to_database` and `display_number_of_inserted_rows` functions signatures.

The second task should be triggered only once the first one succeeds.
The third one should be triggered only once the second one succeeds.
The fourth one should be triggered only once the third one succeeds.

For the `load_to_database` function you should use `pandas` and its [`to_sql` function](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_sql.html) that will directly fill the table for you. However, to benefit from this function, you have to provide a database connection (which is different than an Airflow connection). To make it easier, we already provided a function named `create_connection_from_hook` that create a database connection from an Airflow hook and that you will have to pass to your `to_sql` function.

Moreover, as said just above, we want you to print the number of inserted rows in your second task. Until now, when you had to pass data through tasks you always save it into files. For this last task, you will use [Airflow xcoms](https://airflow.apache.org/docs/apache-airflow/stable/concepts/xcomss.html) to transfer data from `load_to_database` to `display_number_of_inserted_rows`

Finally, as we want your DAG to be [idempotent](https://en.wikipedia.org/wiki/Idempotence), you will have first to remove data from the current date before inserting new data.

As always, once your confident with what you have done, run the following command:

```bash
make test_load_dag
```

Do not hesitate to connect to Adminer and check the content of your Database.

Then, save your work in progress on GitHub 💾

## Optional Google Cloud

This part will guide you to load your data to BigQuery, but as mentioned, it is optional.

In order to use BigQuery you will have to create the Airflow connection. This time, you will do it directly from the Airflow UI. Let's start by launching a local Airflow:

```bash
docker-compose up
```

Then, hover the `Admin` tab and select `Connections`. Click on the white cross to add a new record:
- name the `Connection Id` `google_cloud_connection`
- set the `Connection Type` to `Google Cloud`
- copy paste the whole content of your `service-account.json` to the `Keyfile JSON`

To make your life easier, you will use the `GCSToBigQueryOperator` that will allow you to directly load file to BigQuery from Google Cloud Storage without using a hook. In order to use it, you need to push your local data to Google Cloud Storage. First, let's start by opening your google cloud console and create a bucket named `name-silver` (once again, replace with your first letter of first name and whole last name) and let the default parameters for that bucket.

Once the bucket creation is is done, let's move to your DAG creation. Start by creating an `optional_google_cloud.py` in which you will create a DAG named `optional_google_cloud` with the same arguments as the other ones.

This dag needs 5 tasks:
- an [ExternalTaskSensor](https://airflow.apache.org/docs/apache-airflow/stable/howto/operator/external_task_sensor.html) with a `task_id` named `transform_sensor` that should wait for the DAG `transform` to be in a success state, and check its state every 10 seconds for a maximum of 10 minutes (after that it should timeout)
- a [LocalFileSystemToGCSOperator](https://airflow.apache.org/docs/apache-airflow-providers-google/1.0.0/operators/transfer/local_to_gcs.html) with a `task_id` named `upload_local_file_to_gcs` that should load your local silver file to your Google Cloud Storage silver bucket with the same file's name
- a [`BigQueryCreateEmptyDatasetOperator`](https://airflow.apache.org/docs/apache-airflow-providers-google/stable/_api/airflow/providers/google/cloud/operators/bigquery/index.html#airflow.providers.google.cloud.operators.bigquery.BigQueryCreateEmptyDatasetOperator) with a `task_id` named `create_dataset` that should create the `name_tripdata` dataset (once again, replace with the first letter of your first name and your whole last name)
- a [`BigQueryCreateEmptyTableOperator`](https://airflow.apache.org/docs/apache-airflow-providers-google/stable/_api/airflow/providers/google/cloud/operators/bigquery/index.html#airflow.providers.google.cloud.operators.bigquery.BigQueryCreateEmptyTableOperator) with a `task_id` named `create_table` that should create a table named `trips` (once again, replace with the first letter of your first name and your whole last name) in the dataset `name_tripdata` with the proper schema (`month` as a string and `trip_distance` & `total_amount` as floats)
- a [`GCSToBigQueryOperator`](https://airflow.apache.org/docs/apache-airflow-providers-google/stable/_api/airflow/providers/google/cloud/transfers/gcs_to_bigquery/index.html) with a `task_id` named `load_to_bigquery` that should append the content of the `silver` file to the `trips` table

Once your confident with what you have done, run the following command:

```bash
make test_optional_google_cloud
```

Then, take time to launch the DAG from your Airflow UI and check your Google Cloud Storage & BigQuery instances to see if data is coming.
