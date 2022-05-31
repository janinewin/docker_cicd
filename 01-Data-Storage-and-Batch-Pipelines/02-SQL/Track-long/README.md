# Week 1 - Day 2 - Track-long exercise

Yesterday we set up a base Docker Compose with Postgres, FastAPI and Adminer. Today we'll load some data into this database.

The data comes from [the movies dataset](https://www.kaggle.com/rounakbanik/the-movies-dataset).

## Desired outcome

The students will:

1. for each CSV in this dataset, design a "naive" schema mapping each columns of the CSV (for JSON columns, either use plain TEXT or JSON, we'll manipulate JSON in day 3 and flatten the schema in day 4)
2. add Alembic to the FastAPI app, and run the SQL data migrations designed at step 1. on FastAPI container startup
3. have the students ingest the data by placing the CSVs in a mounted volume and running `COPY...` SQL statements
4. add a command (`Makefile` or `Python`) to wipe the DB and reload the CSVs in it (so they can always alter the DB state, but recreate it from scratch)
