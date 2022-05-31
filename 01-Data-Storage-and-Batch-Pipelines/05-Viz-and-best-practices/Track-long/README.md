# Week 1 - Day 5 - Track-long exercise

So far we have:

- set up a base Docker Compose with Postgres, FastAPI and Adminer. Today we'll load some data into this database.
- loaded a data schema mapping the [the movies dataset](https://www.kaggle.com/rounakbanik/the-movies-dataset), and 
- added a Jupyter lab environment to interact with the datasets and propose a new normalized SQL schema
- loaded periodically the latest comments using an Airflow DAG.

Today, we'll add a dashboard to visualize what we've done so far! The dashboard will have 2 panels:

1. Show the 5 movies with the best rating score (we can define a rating score as the rating's median for instance)
2. Given a movie (add a filter to the panel), show the 10 latest comments

+ anything additional or different the teacher finds cool to display here. The idea is to run SQL queries and build an actual dashboard in Metabase to explore them.

## Desired outcome

The students will:

1. add a Metabase container to the Docker Compose
2. map the Metabase volume with the DB to their host otherwise they'll lose the DB with all the config!
3. configure the DB (choose H2 by default which is embedded, no extra config in theory)
4. connect to the postgres app
5. create the panels
