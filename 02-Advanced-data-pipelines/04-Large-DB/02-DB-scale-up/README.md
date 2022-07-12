# Scaling a database

Database access patterns determine what to optimize for. A database gives us mainly three tools to make queries more efficient:

- adding indexes
- (materialized) views
- a schema redesign

In this exercise, we'll explore all three as well as their pros and cons. We'll use our beloved Postgres database.

We'll load the [Ikea dataset](https://www.kaggle.com/datasets/crawlfeeds/ikea-us-products-dataset).

## Download the data

Download the data under `./data/ikea-raw.json`.
Run your first `make test` after that to show the first token of progress 👍.

<details>
  <summary markdown='span'>💡 Hint</summary>

  `wget` or `scp` from the CHEATSHEET.md
</details>

## Data transformation with Pandas

- We'd like this JSON data as a Parquet file first.
- Run a quick transformation (don't change the data types just yet) sing Pandas and save the Parquet file under `./data/ikea-parquet.csv`.

Write the following functions in `lwdb/db.py`:

- `def json_to_df(...)` to convert the JSON to a Pandas DataFrame
- `def save_df_to_parquet(...)` to store this DataFrame to a Parquet file

<details>
  <summary markdown='span'>💡 Hint</summary>

  Look at a first few lines of the JSON, in the command line do:
  ```bash
  cat ./data/ikea-raw.json | python3 -m json.tool | head -n20
  ```
</details>

### Column types

Now let's look at the columns, do they look like they all have the right type? Cast the columns with string type to `float` or `"Int64"` in the function `def cast_columns(...)` when it seems appropriate.

Then save the new DataFrame to `./data/ikea-cols.csv` after filling in the `def save_df_to_csv(...)` function and running it.

<details>
  <summary markdown='span'>💡 Hint</summary>

  You'll need a combination of `pandas.to_numeric` and `df[column].astype("Int64")`.
</details>

## Start a database

Start a Postgres database using Docker-Compose. There are multiple examples from the previous days. Make sure:

- you specify and use the following environment variables in a `.env` file `POSTGRES_PASSWORD=xxx`
- `POSTGRES_DB` is set to `db` and `POSTGRES_USER` is set to `lewagon` in the environment variables.

<details>
  <summary markdown='span'>💡 Hint</summary>

  Fill in the `.env` with `POSTGRES_PASSWORD=xxx` and have the following block in the Postgers service:

  ```yml
  environment:
  - POSTGRES_DB=db
  - POSTGRES_PASSWORD=$POSTGRES_PASSWORD
  - POSTGRES_USER=lewagon
  ```
</details>

## Create the schema mapping the CSV schema

Fill in `./sql/prep_schema.sql`, a few columns are already given.

<details>
  <summary markdown='span'>💡 Hint</summary>

  There should be as many columns in the table as there are in the CSV.
</details>

## Load the CSV data into the Postgres table

Remember the `COPY <table> FROM ...` from past days. Write the `COPY` command into `./sql/prep_load.sql` and execute it to load the CSV into the table.

<details>
  <summary markdown='span'>💡 Hint</summary>

  Don't forget that the CSV file must be accessible to the Docker container 🐳 while running! What does it imply?
</details>

## Query time!

Let's write a few queries to this medium-sized database.

1. **Q1.** Select all products with a given SKU of `605.106.40`. Write to `sql/q1-v1-select-sku.sql`.
2. **Q2.** Get all products mentioning the words `chair` and `armrest`. Write to `sql/q2-v1-search-chair.sql`
3. **Q3.** Count the number of countries Ikea sells to. Write to `sql/q3-v1-count-countries.sql`.

We provide a function `def query_perf(...)` in `lwdb/db.py` to measure the performance of these queries. Write the performance numbers to `perf.json`.

Do you think we can do better? Let's try 🐙!

## Indexing

TODO @selim - Finish below

Add a BTree index named `index_sku` to the file `index_btree.sql` and run it.

Now run the first query again, is it faster? Fill in the perf as `q1-v2-select-sku`.

- Explore the types of indexes
- B-Tree indexes, add one, evaluate insert and read performance
- CSV loading and adding / removing an index

## Full-text search

- Load the dataset and search by keyword.
- Add full text search and querying in Postgres.

Now rewrite the second query in `sql/q2-v2-search-chair.sql`, re-run it, is it faster? Fill in the perf as `q2-v2-search-chair`.

## Add a join table for countries

- Add a `countries` table, populate it, remove the `country` column to replace with a `country_id`.

Now rewrite the second query in `sql/q3-v2-count-countries.sql`, re-run it, is it faster? Fill in the perf as `q3-v2-count-countries`.

## (Optional) Bonus questions

- Time the CSV load with and without the SKU index. Notice any difference?

<details>
  <summary markdown='span'>💡 Hint</summary>

  It's good practice to first drop the index, load a large dataset, then re-apply the index if load performance is key.
</details>

- 
