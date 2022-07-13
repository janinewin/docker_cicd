# Scaling a database

Database access patterns determine what to optimize for. A database gives us many tools to make queries more efficient. Assuming the data schema is sensible, adding indexes to the database is the next best thing to work on, that's what will keep us busy in this exercise.

We will use our beloved Postgres database, and load the [Ikea dataset](https://www.kaggle.com/datasets/crawlfeeds/ikea-us-products-dataset).

## Download the data

Download the data under `./data/ikea-raw.json`.
Run your first `make test` after that to show the first token of progress 👍.

<details>
  <summary markdown='span'>💡 Hint</summary>

  Use `wget` or `scp` from the CHEATSHEET.md
</details>

## Data transformation with Pandas

- We'd like this JSON data as a Parquet file first.
- Run a quick transformation (don't change the data types just yet) sing Pandas and save the Parquet file under `./data/ikea-raw.parquet`.

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

**💡 Pro tips:** How to run the SQL queries and get timings:

```bash
docker exec -it <name of your Postgres container> /bin/bash
```

followed by (now that you're in the container)

```bash
psql -U lewagon -d db
```

to get into a PSQL interactive shell and be able to type SQL queries.

Then type `/timing` in the PSQL shell, you should see `Timing is on.`.

### Queries

1. **Q1.** Select all products with a given SKU of `605.106.40`. Write to `sql/q1-v1-select-sku.sql`.
2. **Q2.** Count the number of products mentioning the words `chair` and `armrest` in the `raw_product_details` column. Write to `sql/q2-v1-search-chair.sql`

We provide a function `def query_perf(...)` in `lwdb/db.py` to measure the performance of these queries. Write the performance numbers to `perf.json` **in milliseconds**.

Do you think we can do better? Let's try 🐙!

## Indexing

Add a BTree index named `index_sku` to the file `index_btree.sql` and run it.

Nothing better but the official [Postgres documentation](https://www.postgresql.org/docs/current/sql-createindex.html) to figure out how to create the index 🙌.

<details>
  <summary markdown='span'>💡 Hint</summary>

  Replace what's between `<>` below:
  `CREATE INDEX <index name> ON <table> (<column>);`

  Indexes are BTrees by default.
</details>

Now run the first query again, is it faster? Fill in the `perf.json` file, as `q1-v2-select-sku`.

## Full-text search

First of all, the `raw_product_details` column is HTML, not super friendly to search into. Let's create a new column `raw_product_details_text` and extract only the text from this HTML. You can use the SQL transformation below for the new column:

```sql
regexp_replace(raw_product_details, E'<[^>]+>', ' ', 'gi')
```

<details>
  <summary markdown='span'>💡 Hint</summary>

  - First create the column `raw_product_details_text`.
  - Then update its values using the transformation above.
</details>

Add the SQL code in `sql/add_text_col.sql`.

Now that we have a suitable text column, we'd like to add a **search engine** to our database! It would be nice to search for keywords in the product details.

Postgres can index keywords efficiently in text columns using the `GIN` index on a `tsvector`. Essentially, text is parsed into a [tsvector](https://www.postgresql.org/docs/current/datatype-textsearch.html) (check out the examples to understand how Postgres reads text vectors). Then, a GIN index is used to speed up lookups by keywords.

Read the [official documentation, section 12.2.2](https://www.postgresql.org/docs/current/textsearch-tables.html#TEXTSEARCH-TABLES-INDEX). 

Note that there are two ways to index a text column. Either index it directly by having an on-the-fly transform to `tsvector`, OR (recommended) create a `tsvector` column, then index that column with the GIN index.

We'll follow the second method. Add the new `tsvector` column, name it `textsearchable_raw_product_details_text`, and then index it with the GIN index. Call the index `index_raw_product_details_text`. It's a bit hard, so after giving it a shot first, please feel free to check out the walk through hint below 👇.

<details>
  <summary markdown='span'>💡 Hint</summary>

  First create the column
  
  ```sql
  ALTER TABLE <table name>
  ADD COLUMN <new tsvector column name> tsvector
  GENERATED ALWAYS AS (to_tsvector('english' <text column name>)) STORED;
  ```

  then add the index

  ```sql
  CREATE INDEX <index name>
  ON <table name>
  USING GIN (<new tsvector column name>);
  ```
</details>

Now rewrite the second query in `sql/q2-v2-search-chair.sql`. The [bottom of the official documentation, section 12.2.2](https://www.postgresql.org/docs/current/textsearch-tables.html#TEXTSEARCH-TABLES-INDEX) tells you all about running fast text queries against the `tsvector`, indexed column.

<details>
  <summary markdown='span'>💡 Hint</summary>

  Break down the query as:
  
  ```sql
  SELECT count(*)
  FROM ikea_products
  WHERE raw_product_details_text @@ to_tsquery('chair & armrest');
  ```
</details>

Re-run it, is it faster? Fill in the perf as `q2-v2-search-chair`.

## (Optional) Bonus questions

- Time the CSV load with and without the SKU index. Notice any difference?

<details>
  <summary markdown='span'>💡 Hint</summary>

  It's good practice to first drop the index, load a large dataset, then re-apply the index if load performance is key.
</details>
