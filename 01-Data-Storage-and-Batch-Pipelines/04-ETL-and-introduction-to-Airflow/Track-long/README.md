# Week 1 - Day 4 - Track-long exercise

So far we have:

- set up a base Docker Compose with Postgres, FastAPI and Adminer.
- loaded a data schema mapping the [the movies dataset](https://www.kaggle.com/rounakbanik/the-movies-dataset), and
- added a Jupyter lab environment to interact with the datasets and propose a new normalized SQL schema

In the exercise 2, we built a local ETL infrastructure with Apache Airflow. In today's track long exercise, we'll adapt this ETL to load every 5 minutes new comments about the movies that we have loaded into the database.

## Desired outcome

The students will:

1. add Airflow to the current Docker-compose
2. write a script that fetches n comments from the past 5 minutes
3. add a table to the DB for these comments (movie_id + comment data columns)
4. load the comments in the DB


This long track exercise is quite similar to what you have done so it should be easier to implement.

Make sure your terminal is in the current exercise folder and let's start by creating a local Airflow database for pytest by running:

```
make init_db
```

As before, create an `.env` file and set `POSTGRES_PASSWORD` to the value of your choice.

Take time to open the `dags/long_track.py` and discover the functions signatures that we have added to help you.

## DAG Instructions

First, let's focus on creating the proper DAG configuration (no tasks or python functions needed for now).

You need to create a dag with the following requirements:
- it should be named `long_track`
- it should have a start date equal to yesterday
- it should have a description saying `A simple to DAG to fetch and load last movies' comments`
- it should not catchup the missing runs
- it should be scheduled to run every 5 minutes
- it should run no matter if the previous runs succeed

Once, you are confident with your code run:
```
make test_dag_config
```

## Tasks Instructions

Then, we want you to create the tasks that your DAG will use. This time we will create less tasks that will do more things.

You need two tasks:

- A [PostgresOperator](https://airflow.apache.org/docs/apache-airflow-providers-postgres/stable/_api/airflow/providers/postgres/operators/postgres/index.html#module-airflow.providers.postgres.operators.postgres) with a `task_id` named `create_comments_table` that should create a table named create_comments_table with four columns (`id`, `movie_id`, `comment` and `rating` that should be a `primary key`, a not null `integer` column, a not null `varchar` column and a not null `integer` column again).

- A `PythonOperator` with a `task_id` named `get_and_insert_last_comments` that should trigger the `get_and_insert_last_comments` function with the proper arguments.

The second task should be triggered only after the first one's success.

Once you are confident with your code run:
```
make test_tasks_configs
```

Once you passed the tests, launch your Airflow instance and open http://localhost:8080/home to see how your DAG looks.

You should see your four tasks. Turn the dag on and see what happens! It should be all green as your tasks called functions that do not do anything for now.

## Python Functions Instructions

As for the previous exercises, we have added the signatures of 4 functions. This is your turn to implement them in the current order.

Once you are confident with your code run:
```
make test_python_functions
```

Now, you should be able to trigger the DAG, see green results and have your `comments` table being filled.
