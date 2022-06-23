# Track-long exercise - Schema migration

So far we have:

- set up a base Docker Compose with Postgres, FastAPI and Adminer.
- loaded a data schema mapping the [the movies dataset](https://www.kaggle.com/rounakbanik/the-movies-dataset).

Well done 🧠!

As you've noticed, some of the data in the CSVs didn't exactly look like a straightforward type. Rather, it was a JSON list stored in one column.

**Task: take a peek at the CSV file on the [web viewer Data Explorer](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset)**

See? Today we'll manipulate this JSON with Python, to flatten the columns, and then we'll load it up back to Postgres.

**Goal: by the end of the exercise we'll have a database loaded with the schema in `new_schema.sql`. Take a look at it to understand our aim.**

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

### Start from the end, running the file

The last blocks in the code are
- the function `def parse_args():`
- a strange looking `if __name__ == "__main__":` block

If you've looked at other Python projects in the past, you might have already seen the last one.

We can consider that there are two kind of Python files:
- library files. Not meant to be run directly, but imported throughout a project, to not rewrite the same function or class whenever it needs to be used.
- executable files. These files are meant to be called with `python /path/to/file.py`.

When a file is imported, a global variable called `__name__` is automatically set by Python. When a file is executed, this variable is set to the value `__main__`. Therefore, checking is `__name__ == "__main__"` is the way to know whether a file is being executed with `python /path/to/file.py` or simply imported from another Python file with `import ...`.

Here, we'd like to execute `transform.py`, and we'd like to pass arguments to it. Furthermore, we'd like to get some auto-generated documentation when we run it, by say calling `python transform.py -h` (`-h` stands for `help`).

The [argparse](https://docs.python.org/3/library/argparse.html) library comes to the rescue party 🎊!

First, we create a parser

```python
import argparse

...

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--movies", required=True, help="Raw movies CSV filepath")
    parser.add_argument("--out", required=True, help="Output directory")
    return parser.parse_args()
```

This function creates a new argparse.ArgumentParser(), and adds two arguments `--movies` and `--out`. Check out the file, their description is pretty self-explanatory.

Now let's run `python lwtransform/transform.py -h`. This generates documentation anyone using the file can get, so they know they can and must pass two arguments when running it, `--movies <path to movies_metadata.csv>` and `--out <path to the output directory>`.

Then we call this parser and pass the parsed arguments to the main function (all of this wrapped in our `if __name__ == "__main__"` check, which makes sure you're executing the file and not importing it).

```python
if __name__ == "__main__":
    _args = parse_args()
    movies_to_new_tables(raw_movies_metadata_csv_fp=_args.movies, output_dir=_args.out)
```

Calling `_args = parse_args()` calls the parser we wrote, and we pass its values to the main function `movies_to_new_tables`, which we'll now dive into ⛏️.

### The main function `movies_to_new_tables`

Most data transformation jobs are what we call `pipelines`, which are a sequence of steps, in which the outputs of previous steps can be the inputs of subsequent steps.

What are we trying to achieve?

1. There's this file `data/movies_metadata.csv`, it's got a bunch of tabular data, some columns aren't quite in the right format. Let's load this data with the `load_and_clean_movies` function.
2. Then we'll work on this dataset to extract additional information we need to create these new additional tables. In our case, that's the `extract_lists` function. That's the role of the `extract_lists` function.
3. Then we use both steps 1. and 2. to generate the new tables. That's the `make_new_tables` function, **we won't look into it in this exercise, just assume it works!**.
4. We'll need to save the new tables in CSVs, so we can load them back into the database. You'll write this bit, by calling the function `save_new_tables_to_csvs` in the right spot with the right arguments.

**Take a close look at the content of the functions `load_and_clean_movies` and `make_new_tables`**

**Now, open an interactive Jupyter lab session and play with this data**

- Open Jupyter lab by calling `poetry run jupyter lab`
- Create a new file by clicking the blue "+" button at the top left, select a Python3 kernel.

Type,

```python
from lwtransform.transform import *
```

Now create two variables and give them values
- `raw_movies_metadata_csv_fp=<fill me>`: the path to the `movies_metadata.csv` file
- `output_dir`: the path to your `data` directory

Then copy and paste the contents of the function

```python
def movies_to_new_tables(raw_movies_metadata_csv_fp: str, output_dir: str):
```

into a new cell.

```python
pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)
original_movies_df = load_and_clean_movies(raw_movies_metadata_csv_fp)
genres_list, production_companies_list, production_countries_list, spoken_languages_list = extract_lists(original_movies_df)
tags_df, tags_map_df = make_new_tables(original_movies_df, genres_list, production_companies_list, production_countries_list, spoken_languages_list)
```

This will evaluate all this code interactively.

**Play with the newly created DataFrames `tags_df` and `tags_map_df`. Create and evaluate a new cell for each of these values**.

<details>
  <summary markdown='span'>💡 Hint</summary>
  - Click `+` to insert a cell below
  - Copy `tags_df` in the cell
  - Evaluate the cell with the play button
  - You should see a nice looking table 
</details>

Now do the same with `original_movies_df.loc[:, ["id", "genres", "original_title"]]`. Notice the JSON looking column `genres`. Now see how we extracted the tags from the original database? That's what the function `make_new_tables` was responsible for.

Now these tables should look like the schema we had in mind, in `new_schema.sql`.

**Add the `save_new_tables_to_csvs` in the `lwtransform/transform.py` with the right arguments and run `poetry run python lwtransform/transform.py --movies ./data/movies_metadata.csv --out ./data/`**

Done?

Type `head data/tags.csv`, does the data look like what you've seen in the Jupyter lab session?

Yes? 🎉 . We're done for the Python part here!

## Postgres database

### Start Postgres

Now we'll load this data into Postgres.

**Let's take a look at the `docker-compose.yml` file. You'll see that we have added comments to explain each section.**

As you've seen in the `docker-compose.yml` file, there's one environment variable that needs to be set in a `.env` file, so create a `.env` file and set this value. Use the `env-template` file as a reference.

Now, we're ready to run the database ; for that, let's run the following Docker Compose command.

```
docker-compose up -d
```

**The `-d` argument started it in the background, how do we check the logs?**
<details>
  <summary markdown='span'>💡 Hint</summary>
  - First reflex! [Check the doc](https://docs.docker.com/engine/reference/commandline/compose_logs/). Caveat: the doc uses the syntax `docker compose`, we should use the syntax `docker-compose`, in one word, with a `-` in the middle.
  - Try `docker-compose logs -ft` to add time and track the logs.
  - Exit with CTRL+C.
</details>

### Set-up Adminer

Now open Adminer in the browser, after a doing a port tunnel in VSCode (see the cheatseet for that): [http://localhost:8089](http://localhost:8089).

The first page should prompt you to connect to the database.

- System: PostgreSQL
- Server: `database` <- this takes the name of our service in Docker-Compose 🤯
- User and database: `postgres`
- Password: the one you set in `.env`

You're in! 🤠

### Create the database schema

Take a look at `new_schema.sql`, there is one hole, can you fix it?

<details>
  <summary markdown='span'>💡 Hint</summary>
  The syntax is very similar to the `CREATE TABLE ratings` block!
</details>

### Load the data

Now we'll load the CSV data into these tables. The SQL code is in `load.sql`, but there is one hole, can you fix it?

<details>
  <summary markdown='span'>💡 Hint</summary>
  Similar to `COPY tags_map`...
</details>

Run the contents of the `load.sql` file (just copy paste it then execute the query).

<details>
  <summary markdown='span'>💡 Hint</summary>
  There's a `SQL command` link for that on Adminer.
</details>

### Select queries

**Let's take a peek at the tables now 😏. Run a few queries, click around Adminer to explore it.**

- `select * from movies_metadata limit 5;`
- `select * from tags limit 5;`
- `select distinct name from tags;`
- `select * from tags_map limit 5;`

**Write a query to count the number of movies with the genre 'Drama'**

<details>
  <summary markdown='span'>💡 Hint</summary>
  Try filling in the ?? below:
  - `select count(*) from tags_map where tag_name='??' and tag_value = '??'`
</details>

Great work 👏. We've re-structured our database and now our queries look a lot saner and easier to use. We're well set up for the rest of the week's track-long!
