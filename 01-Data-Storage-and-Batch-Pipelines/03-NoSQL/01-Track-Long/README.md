# Track-long exercise - Schema migration

So far we have:

- set up a base Docker Compose with Postgres, FastAPI and Adminer. Today we'll load some data into this database.
- loaded a data schema mapping the [the movies dataset](https://www.kaggle.com/rounakbanik/the-movies-dataset).

Well done 🧠!

As you've noticed, some of the data in the CSVs didn't exactly look like a straightforward type. Rather, it was a JSON list stored in one column.

**Task: take a peek at the CSV file on the [web viewer Data Explorer](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset)**

See? Today we'll manipulate this JSON with Python, to flatten the columns, and then we'll load it up back to Postgres.

## Introduction

### Let's discover the Python packages we'll use

Open the `pyproject.toml` file. We use Poetry for Python packages management. If you haven't already, [read up about the pyproject.toml file](https://python-poetry.org/docs/pyproject/). In this exercise, we care mostly about these two lines:

```toml
pandas = "^1.4.2"
```
to manipulate tabular (CSV) data.

```toml
psycopg2-binary = "^2.9.3"
```
to connect to the Postgres database.

```toml
jupyterlab = "^3.4.2"
```
to play with data interactively in Python.

```toml
lewagonde = { path = "../../../common/lewagonde/", develop = true }
```

**What could this last snippet mean? It looks different from the others doesn't it?**

<details>
  <summary markdown='span'>💡 Hint</summary>
  - Take a look at the `add` section, specifically "If you want the dependency to be installed in editable mode" of the [Poetry docs](https://python-poetry.org/docs/cli/#add).
  - Did you find the `lewagonde` directory within `common` in this Github repository?
</details>

We've written our own Python package, packaged with Poetry. We're importing it here. We'll use some of its functionality below 👇.

### Download the files

From the [webpage](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset?select=movies_metadata.csv), download `movies_metadata.csv` into a `data` directory to create.

## Transform - step by step

In the file `lwtransform/transform.py`, we've written pipeline code to transform this `data/movies_metadata.csv` file into several, normalized files. We'll walk through the transformation code step by step, and we'll need your help for the final step, saving the CSV files!

By the end of the exercise, the command

```
poetry run python lwtransform/transform.py --movies ./data/movies_metadata.csv --out ./data/
```

should work and produce 3 new files in the `./data` directory:

```
$ tree data/
data/
├── movies_metadata.csv
├── movies_metadata_normalized.csv
├── tags.csv
└── tags_map.csv
```

TODO @selim - Add walkthrough here.

## Postgres database

### Start Postgres

Now we'll load this data into Postgres. For that, let's run the following Docker Compose command

```
docker-compose up -d
```

Let's take a look at the `docker-compose.yml` file.

TODO @selim - Break down this file

### Create the database schema

Take a look at `new_schema.sql`, there is one hole, can you fix it?

TODO @selim - Add hints

### Load the data

Now we'll load the CSV data into these tables. The SQL code is in `load.sql`, but there is one hole, can you fix it?

TODO @selim - Add hints

Now open Adminer and run the contents of this file (just copy paste it).

### Select queries

**Let's take a peek at the tables now 😏.**

TODO @selim - Add hints

**Write a query to count the number of movies with the genre 'Drama'**

TODO @selim - Add hints and tests.

**Optional - Write a SQL query to group the movies by genre**

TODO @selim - Add hints.
