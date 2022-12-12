### 🎯 Goal

In this challenge, you will focus on creating a more complex **ETL**, without caring about setting-up the docker-compose.

The goal is to have a DAG running every day that will:
- (**Extract**) Downloads a Chuck Norris' joke, using this [api](https://api.chucknorris.io), saving them as [JSON](https://en.wikipedia.org/wiki/JSON) into your "Lake" (our local `data` folder)
- (**Transform**) Translates it to Swedish, saving them again in the "Lake"
- (**Load**) Inserts them it into your "Data Warehouse" (our local `db` postgres used also to store airflow metadata)

As for the previous exercise, we split the instructions in four parts to help you create this local ETL.

# 1️⃣ Setup ⚙️

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

# 2️⃣ DAG Instructions ↪

First, let's focus on creating the proper DAG configuration (no tasks or python functions needed for now).

You need to create a DAG with the following requirements:
- it should be named `local_etl`
- it should be scheduled to run every day, with a start date equal to five days ago (so we'll simulate 5 runs)
- it should have a description saying `A local etl`
- it should catchup the missing runs
- it should run only if the previous runs succeed

🧪 Once, you are confident with your code run:

```bash
make test_dag_config
```

## Tasks 🏋️

Then, we want you to create the tasks that your DAG will use. This time you will create more tasks that will do less things.

You need four tasks:

### a) A `create_swedified_jokes_table` task_id
- as a [PostgresOperator](https://airflow.apache.org/docs/apache-airflow-providers-postgres/stable/_api/airflow/providers/postgres/operators/postgres/index.html#module-airflow.providers.postgres.operators.postgres) :
- that should create a table named `swedified_jokes` with 3 columns:
- `id` (serial primary)
- `joke` (varchar not null)
- `swedified_joke` (varchar not null)

### b) `extract` task_id
- as a [BashOperator](https://airflow.apache.org/docs/apache-airflow/stable/howto/operator/bash.html):
- that [curl](https://en.wikipedia.org/wiki/CURL) a random Chuck Norris' joke from [https://api.chucknorris.io](https://api.chucknorris.io).
- The joke should be saved to the bronze folder under the name `joke_{execution_date}.json` where {execution_date} corresponds to the execution date of the Airflow dag (for instance: */app/airflow/data/bronze/joke_20220521.json*). 💡 Check [airflow template variables](https://airflow.apache.org/docs/apache-airflow/stable/templates-ref.html)

### c) `transform` task_id
- as a [PythonOperator](https://airflow.apache.org/docs/apache-airflow/2.2.0/howto/operator/python.html)
- that should trigger the `transform` function with the proper arguments (don't fill the python function yet)
- The transformed joke should be saved to the silver folder under the name joke_{execution_date}.json (for instance: */app/airflow/data/silver/joke_20220521.json*).


### d) `load` task_id
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

## Python Functions 🐍

To help you, we have already added the signature of 6 functions. This is now your turn to implement them in the current order.

🧪 Once you are confident with your code run:
```bash
make test_python_functions
```

Now, you should be able to trigger the DAG, see green results and have your `swedified_jokes` table being filled. Check it out on DBEAVER!

See below for tips if you are stuck!

# 4️⃣ Airflow Pro Tips 💡

## 🐛 Debugging in Airflow ?

**Reset Airflow DB**
In case you want to replay your challenge history from scratch, you can reset your airflow metadata database as if the were never run before

```bash
docker-compose exec webserver poetry run airflow db reset
```

Otherwise, you can also `sudo rm -rf database` entirely, but that's not a great skill to master in real life ;)

**Check logs on Airflow UI**
It's our recommended approach to begin with. Below, the second task of our first run has failed. And 4 other run are planned and running (they wait for the next 4 days to be finish)
You can click on "Log" to inspect logs

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/airflow_failing.png">



**Check logs from your Terminal**

You can access your logs from your terminal, but mixing logs of 3 services at once can be messy. Simply open 3 terminal, each with one of the commands:

```bash
docker-compose logs -f postgres
docker-compose logs -f scheduler
docker-compose logs -f webserver
```

**Check logs from logs folder**
You should be able to see the exact same information in your `logs` folder, which is precious to grep for "ERROR" lines etc...!

## 🧪 Testing in Airflow ?

It can be interesting to read our tests to learn how to test your DAGs.

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

# 🏁 Congratulation!

Run `make test` to create test_output.txt, then git add, commit and push your code so we can track your progress!
