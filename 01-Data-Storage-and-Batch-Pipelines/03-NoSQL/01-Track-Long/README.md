# Track-long exercise - Schema migration

TODO @selim
- Add tests
- Expand README

-- NOTE FOR REVIEWERS -> Not ready for review - skip to exos 2 and 3 which are ready --

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
