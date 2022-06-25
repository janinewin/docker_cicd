### Introduction

In this challenge, you will create a more complex ETL.

The goal is to have a DAG running every day that will:
- downloads a Chuck Norris' joke (Extract)
- translates it to Swedish (Transform)
- inserts it into your PostgreSQL database (Load)

For the Chuck Norris' joke, you will use this [api](https://api.chucknorris.io).

You will save the jokes and their translated versions to [JSON](https://en.wikipedia.org/wiki/JSON) before inserting them to your PostgreSQL database that will play the roles of "Data Lake" (your JSON files) and "Data Warehouse" (your PostgreSQL database).

As for the previous exercise, we split the instructions in four parts to help you create this local ETL.

## DAG Instructions

First, let's focus on creating the proper DAG configuration (no tasks or python functions needed for now).

You need to create a DAG with the following requirements:
- it should be named `local_etl`
- it should have a start date equal to five days ago
- it should have a description saying `A local etl`
- it should catchup the missing runs
- it should be scheduled to run every day
- it should run only if the previous runs succeed

Once, you are confident with your code run:

```bash
make init_db
```

and then

```
$ make test_dag_config
```

## Tasks Instructions

Then, we want you to create the tasks that your DAG will use. This time you will create more tasks that will do less things.

You need four tasks:

- A [PostgresOperator](https://airflow.apache.org/docs/apache-airflow-providers-postgres/stable/_api/airflow/providers/postgres/operators/postgres/index.html#module-airflow.providers.postgres.operators.postgres) with a `task_id` named `create_swedified_jokes_table` that should create a table named `swedified_jokes` with three columns (`id`, `joke` and `swedified_joke` that should be a `primary key` and two not null `varchar` columns).
- A [BashOperator](https://airflow.apache.org/docs/apache-airflow/stable/howto/operator/bash.html) to [curl](https://en.wikipedia.org/wiki/CURL) a random Chuck Norris' joke from [https://api.chucknorris.io](https://api.chucknorris.io) with a `task_id` named `extract`. The joke should be saved to the bronze folder under the name `joke_{execution_date}.json` where {execution_date} corresponds to the execution date of the Airflow dag (for instance: **/opt/airflow/data/bronze/joke_20220521.json**).
- A `PythonOperator` with a `task_id` named `transform` that should trigger the `transform` function with the proper arguments. The transformed joke should be saved to the silver folder under the name joke_{execution_date}.json (for instance: **/opt/airflow/data/silver/joke_20220521.json**).
- A `PythonOperator` with a `task_id` named `load` that should trigger the `load` function with the proper arguments.


We have already added the `transform` and `load` functions signatures, but again: **for this part, you don't have to fill the functions but only to create the Airflow tasks that will call them.**

The second task should be triggered only after the first one's success.
The third task should be triggered only after the second one's success.
The fourth task should be triggered only after the third one's success.

Once you are confident with your code run:
```
$ make test_tasks_configs
```

Once you passed the tests, launch your Airflow instance and open [localhost](http://localhost:8080/home) to see how your DAG looks.

You should see your four tasks. Turn the DAG on and see what happens! It should be all green 🟢 as your tasks called functions that do not do anything for now.

## Python Functions Instructions

To help you, we have already added the signature of 6 functions. This is now your turn to implement them in the current order.

Once you are confident with your code run:
```
$ make test_python_functions
```

Now, you should be able to trigger the DAG, see green results and have your `swedified_jokes` table being filled.
