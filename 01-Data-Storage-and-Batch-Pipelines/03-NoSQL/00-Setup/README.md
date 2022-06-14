# Day 03 - NoSQL

Today we will:

- Discover alternatives to SQL with NoSQL databases
- Gain practical experience setting up and using some NoSQL databases for specific use cases
- Be introduced to several serialization formats, from the simplest text-based CSVs to more advanced binary formats like Protobuf or Parquet

## Setup

Just run `poetry install` in the parent directory which contains the `pyproject.toml`. We'll use this same Python configuration throughout the day.

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

## Test your setup

1. From any directory in your terminal, typing `which python` should show the correct path to your Python install.
2. Run all the tests under `00-Setup-Exercise` with: `pytest 00-Setup-Exercise/tests/*`.
