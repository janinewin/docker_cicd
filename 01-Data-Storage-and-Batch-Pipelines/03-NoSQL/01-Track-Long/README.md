# Day 03 - NoSQL

Today we will:

- Discover alternatives to SQL with NoSQL databases
- Gain practical experience setting up and using some NoSQL databases for specific use cases
- Be introduced to several serialization formats, from the simplest text-based CSVs to more advanced binary formats like Protobuf or Parquet

## Setup

Just run `poetry install` in the parent directory which contains the `pyproject.toml`. We'll use this same Python configuration throughout the day. Let's take a moment to check what's installed. Take a peek into the `pyproject.toml`.

You'll see that we install the following database client packages:

- `psycopg2-binary` for [Postgres](https://www.postgresql.org/) and [TimescaleDB](https://www.timescale.com/) (time series)
- `neo4j` for the [Neo4J](https://neo4j.com/developer/python/) database
- `elasticsearch[async]` to communicate asynchronously with [ElasticSearch](https://www.elastic.co/fr/elasticsearch/) using Python's `async/await` keywords.

For data serialization formats, we install

- `protobuf` for Google's [Protobuf](https://developers.google.com/protocol-buffers) serialization format
- `pyarrow` for [Parquet](https://arrow.apache.org/docs/python/getstarted.html)
- `pandas` to manipulate tabular data, see [Pandas](https://pandas.pydata.org/)
- `openpyxl` to manipulate [Excel files in Python](https://openpyxl.readthedocs.io/en/stable/)

Throughout these exercises today we'll learn to play with these various databases, and data exchanges formats. You can run `poetry install` in this directory and reuse this install for the whole day.

Once installed, we'll add the path to this Python installation in our `PATH` environment variable. For that, run `poetry run which python` and copy the full path minus the last word `python`. For instance, if the output is `/home/myname/.cache/pypoetry/virtualenvs/w1d3-0uMKUenS-py3.8/bin/python`, just keep `/home/myname/.cache/pypoetry/virtualenvs/w1d3-0uMKUenS-py3.8/bin/`.

Now open the file `~/.bashrc` in VSCode (just type `code ~/.bashrc` in your VSCode terminal), and add the last line (or edit it if you've done that in previous days):

(of course, replace by your real path)
```
PATH=/Users/myname/Library/Caches/pypoetry/virtualenvs/w1d3-0uMKUenS-py3.8/bin/:$PATH
PYTHONPATH=<path/to/03-NoSQL>:$PYTHONPATH
```

## Track-long exercise

So far we have:

- set up a base Docker Compose with Postgres, FastAPI and Adminer. Today we'll load some data into this database.
- loaded a data schema mapping the [the movies dataset](https://www.kaggle.com/rounakbanik/the-movies-dataset).

As you've noticed, some of the data in the CSVs didn't exactly look like a straightforward type. Rather, it was a JSON list stored in one column. Today we'll manipulate this JSON with Python and with Postgres.

### Desired outcome

The students will:

1. Add a Jupyter lab container to the Docker compose stack (with data science libraries loaded)
2. Load a sample of the data using Pandas + a Postgres connection
3. Write in SQL the question "How many movies are there with the 'Drama' genre in this dataset?"
4. Now try to group by movies by genre. Tough one right? The current schema is too _raw_, manipulate some of the JSON columns and create new tables such that there is no JSON stored in the database anymore. This is called normalizing the schema.
5. Load the new data format into the database.
6. Rewrite the question line 3 with the new schema, and answer question 4 "group by movies by genre".
