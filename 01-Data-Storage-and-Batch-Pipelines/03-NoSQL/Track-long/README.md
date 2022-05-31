# Week 1 - Day 3 - Track-long exercise

So far we have:

- set up a base Docker Compose with Postgres, FastAPI and Adminer. Today we'll load some data into this database.
- loaded a data schema mapping the [the movies dataset](https://www.kaggle.com/rounakbanik/the-movies-dataset), and 

As you've noticed, some of the data in the CSVs didn't exactly look like a straightforward type. Rather, it was a JSON stored in one column. Today we'll manipulate this JSON with Python and with Postgres.

## Desired outcome

The students will:

1. add a Jupyter lab container to the Docker compose stack (with data science libraries loaded)
2. load a sample of the data using Pandas + a Postgres connection
3. manipulate some of the JSON columns to answer questions like "How many actors in movie X?"
4. answer the same question but in SQL
5. propose a newer, normalized, SQL schema
