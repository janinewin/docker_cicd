### 🎯 Goal

In this challenge, you will focus on creating a more complex **ETL**, without caring about setting-up the docker-compose.

The goal is to have a DAG running every day that will:
- (**Extract**) Downloads a Chuck Norris' joke, using this [api](https://api.chucknorris.io), saving them as [JSON](https://en.wikipedia.org/wiki/JSON) into your "Lake" (our local `data` folder)
- (**Transform**) Translates it to Swedish, saving them again in the "Lake"
- (**Load**) Inserts them it into your "Data Warehouse" (our local `db` postgres used also to store airflow metadata)

As for the previous exercise, we split the instructions in four parts to help you create this local ETL.

# 1️⃣ Setup

The Dockerfile and docker-compose are similar to that of previous challenge, with one exception: the entrypoint.sh now contains an additional line:

```bash

airflow connections add 'postgres_connection' \
                    --conn-type postgres \
                    --conn-host "postgres" \
                    --conn-schema "$POSTGRES_DB" \
                    --conn-login "$POSTGRES_USER" \
                    --conn-password "$POSTGRES_PASSWORD" \
                    --conn-port "5432"
```

👉 Naming such connections explicitly is required to interact with the DB "warehouse" in our **load**  stage:

```python
PostgresOperator(
    sql=... # create warehouse table, insert translated jokes...
    postgres_conn_id='postgres_connection')
```

💡 We didn't need it in our previous challenge as we were not storing anything in a warehouse!

You just have to add your `POSTGRES_PASSWORD` in a new `.env` file, then:

```
docker-compose up
```

You should be able to:
- access airflow webserver on `localhost:8080`
- access airflow db via DBeaver on port `localhost:5433`

# 2️⃣ DAG Instructions

First, let's focus on creating the proper DAG configuration (no tasks or python functions needed for now).

You need to create a DAG with the following requirements:
- it should be named `local_etl`
- it should have a start date equal to five days ago
- it should have a description saying `A local etl`
- it should catchup the missing runs
- it should be scheduled to run every day
- it should run only if the previous runs succeed

🧪 Once, you are confident with your code run:

```bash
make test_dag_config
```

## Tasks Instructions

Then, we want you to create the tasks that your DAG will use. This time you will create more tasks that will do less things.

You need four tasks:

### a) A `create_swedified_jokes_table` task_id
- as a [PostgresOperator](https://airflow.apache.org/docs/apache-airflow-providers-postgres/stable/_api/airflow/providers/postgres/operators/postgres/index.html#module-airflow.providers.postgres.operators.postgres) :
- that should create a table named `swedified_jokes` with 3 columns:
- `id` (serial primary)
- `joke` (varchar not null)
- `swedified_joke` (varchar not null)

### b) A `extract` task_id
- as a [BashOperator](https://airflow.apache.org/docs/apache-airflow/stable/howto/operator/bash.html):
- that [curl](https://en.wikipedia.org/wiki/CURL) a random Chuck Norris' joke from [https://api.chucknorris.io](https://api.chucknorris.io).
- The joke should be saved to the bronze folder under the name `joke_{execution_date}.json` where {execution_date} corresponds to the execution date of the Airflow dag (for instance: */app/airflow/data/bronze/joke_20220521.json*).
- 💡 Check [airflow template variables](https://airflow.apache.org/docs/apache-airflow/stable/templates-ref.html)

### c) A `transform` task_id
- as a [PythonOperator](https://airflow.apache.org/docs/apache-airflow/2.2.0/howto/operator/python.html)
- that should trigger the `transform` function with the proper arguments (don't fill the python function yet)
- The transformed joke should be saved to the silver folder under the name joke_{execution_date}.json (for instance: */app/airflow/data/silver/joke_20220521.json*).


### d) A `load` task_id
- as a `PythonOperator`
- that should trigger the `load` function with the proper arguments (don't fill python function yet)

### Now, arrange your tasks
- The second task should be triggered only after the first one's success.
- The third task should be triggered only after the second one's success.
- The fourth task should be triggered only after the third one's success.

🧪 Once you are confident with your code run:
```bash
make test_tasks_configs
```

Once you passed the tests, launch your Airflow instance and open [localhost](http://localhost:8080/home) to see how your DAG looks.

You should see your four tasks. Turn the DAG on and see what happens! It should be all green 🟢 as your tasks called functions that do not do anything for now.

## 3️⃣ Python Functions 🐍

To help you, we have already added the signature of 6 functions. This is now your turn to implement them in the current order.

🧪 Once you are confident with your code run:
```bash
make test_python_functions
```

Now, you should be able to trigger the DAG, see green results and have your `swedified_jokes` table being filled.

## 💡 Optional: How does our tests work?

It can be interesting to learn how to test your airflow DAGs.

👉 Have a look at your `makefile`, and let's focus on `test_dag_config`

- We don't want to test your code against your "production" database `db`.
- Therefore, everytime you're running `make test_dag_config`, we're creating a local sqlite copy of your postgres db.
- How does it work? We're changing AIRFLOW_HOME to a new temp folder, by default when running `airflow db init`, this will create a brand new airflow project which by default runs a sqlite metadata db.
- You can inspect the 3 files that were created inside `tests/temp`
  - `airflow.db` is the sqlite copy of you postgresdb
  - `webserver_config.py`
  - `airflow.cfg`
    - check line 185: your `sql_alchemy_conn` refers to that local sqlite!
    - compare it to that of your currently running app: `docker-compose exec webserver poetry run airflow config get-value database sql_alchemy_conn`!
- Then we also have to change the postgres hook connection, to add/remove fake jokes to that sqlite DB instead of your postgres! This is why we have to run `tests/scripts/init_connections.sh` in our makefile.

## 🏁 Congratulation! `make test` to create test_output.txt, then add, commit and push your code so we can track your progress!
